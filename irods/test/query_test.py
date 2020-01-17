#! /usr/bin/env python
from __future__ import absolute_import
import os
import sys
import unittest
from datetime import datetime
from irods.models import User, Collection, DataObject, Resource
from irods.exception import MultipleResultsFound, CAT_UNKNOWN_SPECIFIC_QUERY, CAT_INVALID_ARGUMENT
from irods.query import SpecificQuery
from irods.column import Like, Between
from irods import MAX_SQL_ROWS
import irods.test.helpers as helpers


class TestQuery(unittest.TestCase):

    def setUp(self):
        self.sess = helpers.make_session()

        # test data
        self.coll_path = '/{}/home/{}/test_dir'.format(self.sess.zone, self.sess.username)
        self.obj_name = 'test1'
        self.obj_path = '{coll_path}/{obj_name}'.format(**vars(self))

        # Create test collection and (empty) test object
        self.coll = self.sess.collections.create(self.coll_path)
        self.obj = self.sess.data_objects.create(self.obj_path)


    def tearDown(self):
        '''Remove test data and close connections
        '''
        self.coll.remove(recurse=True, force=True)
        self.sess.cleanup()


    def test_collections_query(self):
        # collection query test
        result = self.sess.query(Collection.id, Collection.name).all()
        assert result.has_value(self.coll_path)


    def test_files_query(self):
        # file query test
        query = self.sess.query(
            DataObject.id, DataObject.collection_id, DataObject.name, User.name, Collection.name)

        # coverage
        for column in query.columns:
            repr(column)

        result = query.all()
        assert result.has_value(self.obj_name)


    def test_users_query(self):
        '''Lists all users and look for known usernames
        '''
        # query takes model(s) or column(s)
        # only need User.name here
        results = self.sess.query(User.name).all()

        # get user list from results
        users = [row[User.name] for row in results.rows]

        # assertions
        self.assertIn('rods', users)
        self.assertIn('public', users)


    def test_resources_query(self):
        '''Lists resources
        '''
        # query takes model(s) or column(s)
        results = self.sess.query(Resource).all()

        # check ResultSet.__str__()
        str(results)

        # get resource list from results
        resources = [row[Resource.name] for row in results.rows]

        # assertions
        self.assertIn('demoResc', resources)


    def test_query_first(self):
        # with no result
        results = self.sess.query(User.name).filter(User.name == 'boo').first()
        self.assertIsNone(results)

        # with result
        results = self.sess.query(User.name).first()
        self.assertEqual(len(results), 1)


    def test_query_one(self):
        # with multiple results
        with self.assertRaises(MultipleResultsFound):
            results = self.sess.query(User.name).one()


    def test_query_wrong_type(self):
        with self.assertRaises(TypeError):
            query = self.sess.query(str())


    def test_query_order_by(self):
        # query for user names
        results = self.sess.query(User.name).order_by(User.name).all()

        # get user names from results
        user_names = []
        for result in results:
            user_names.append(result[User.name])

        # make copy before sorting
        original = list(user_names)

        # check that list was already sorted
        user_names.sort()
        self.assertEqual(user_names, original)


    def test_query_order_by_desc(self):
        # query for user names
        results = self.sess.query(User.name).order_by(
            User.name, order='desc').all()

        # get user names from results
        user_names = []
        for result in results:
            user_names.append(result[User.name])

        # make copy before sorting
        original = list(user_names)

        # check that list was already sorted
        user_names.sort(reverse=True)
        self.assertEqual(user_names, original)


    def test_query_order_by_invalid_param(self):
        with self.assertRaises(ValueError):
            results = self.sess.query(User.name).order_by(
                User.name, order='moo').all()


    def test_query_with_like_condition(self):
        '''Equivalent to:
        iquest "select RESC_NAME where RESC_NAME like 'dem%'"
        '''

        query = self.sess.query(Resource).filter(Like(Resource.name, 'dem%'))
        self.assertIn('demoResc', [row[Resource.name] for row in query])


    def test_query_with_between_condition(self):
        '''Equivalent to:
        iquest "select RESC_NAME, COLL_NAME, DATA_NAME where DATA_MODIFY_TIME between '01451606400' '...'"
        '''
        session = self.sess

        start_date = datetime(2016, 1, 1, 0, 0)
        end_date = datetime.utcnow()

        query = session.query(Resource.name, Collection.name, DataObject.name)\
            .filter(Between(DataObject.modify_time, (start_date, end_date)))

        for result in query:
            res_str = '{} {}/{}'.format(result[Resource.name], result[Collection.name], result[DataObject.name])
            self.assertIn(session.zone, res_str)


class TestSpecificQuery(unittest.TestCase):

    def setUp(self):
        super(TestSpecificQuery, self).setUp()
        self.session = helpers.make_session()


    def tearDown(self):
        self.session.cleanup()
        super(TestSpecificQuery, self).tearDown()


    def test_query_data_name_and_id(self):
        # make a test collection larger than MAX_SQL_ROWS (number of files)
        test_collection_size = 3*MAX_SQL_ROWS
        test_collection_path = '/{0}/home/{1}/test_collection'.format(self.session.zone, self.session.username)
        self.test_collection = helpers.make_test_collection(
            self.session, test_collection_path, obj_count=test_collection_size)

        # make specific query
        sql = "select data_name, data_id from r_data_main join r_coll_main using (coll_id) where coll_name = '{test_collection_path}'".format(**locals())
        alias = 'list_data_name_id'
        columns = [DataObject.name, DataObject.id]
        query = SpecificQuery(self.session, sql, alias, columns)

        # register query in iCAT
        query.register()

        # run query and check results
        for i, result in enumerate(query):
            self.assertIn('test', result[DataObject.name])
            self.assertIsNotNone(result[DataObject.id])
        self.assertEqual(i, test_collection_size - 1)

        # unregister query
        query.remove()

        # remove test collection
        self.test_collection.remove(recurse=True, force=True)


    def test_query_data_name_and_id_no_columns(self):
        '''Same test as above, but without providing query columns to parse results.
        Result columns are retrieved by index 0..n
        '''

        # make a test collection larger than MAX_SQL_ROWS (number of files)
        test_collection_size = 3*MAX_SQL_ROWS
        test_collection_path = '/{0}/home/{1}/test_collection'.format(self.session.zone, self.session.username)
        self.test_collection = helpers.make_test_collection(
            self.session, test_collection_path, obj_count=test_collection_size)

        # make specific query
        sql = "select data_name, data_id from r_data_main join r_coll_main using (coll_id) where coll_name = '{test_collection_path}'".format(**locals())
        alias = 'list_data_name_id'
        query = SpecificQuery(self.session, sql, alias)

        # register query in iCAT
        query.register()

        # run query and check results
        for i, result in enumerate(query):
            self.assertIn('test', result[0])
            self.assertIsNotNone(result[1])
        self.assertEqual(i, test_collection_size - 1)

        # unregister query
        query.remove()

        # remove test collection
        self.test_collection.remove(recurse=True, force=True)


    def test_register_query_twice(self):
        query = SpecificQuery(self.session, sql='select data_name from r_data_main', alias='list_data_names')

        # register query
        query.register()

        # register same query again
        with self.assertRaises(CAT_INVALID_ARGUMENT) as ex:
            query.register()

        # check the error message
        self.assertEqual(str(ex.exception), 'Alias is not unique')

        # remove query
        query.remove()


    def test_list_specific_queries(self):
        query = SpecificQuery(self.session, alias='ls')

        for result in query:
            self.assertIsNotNone(result[0])             # query alias
            self.assertIn('SELECT', result[1].upper())  # query string


    def test_list_specific_queries_with_wrong_alias(self):
        query = SpecificQuery(self.session, alias='foo')

        with self.assertRaises(CAT_UNKNOWN_SPECIFIC_QUERY):
            res = query.get_results()
            next(res)

    def test_simultaneous_multiple_AVU_joins(self):
        objects = []
        decoys = []
        try:
            collection = self.coll_path
            filename = 'test_multiple_AVU_joins'
            file_path = '{collection}/{filename}'.format(**locals())
            for x in range(3,9):
                obj = helpers.make_object(self.sess, file_path+'-{}'.format(x))  # with metadata
                objects.append(obj)
                obj.metadata.add('A_meta','1{}'.format(x))
                obj.metadata.add('B_meta','2{}'.format(x))
                decoys.append(helpers.make_object(self.sess, file_path+'-dummy{}'.format(x)))   # without metadata
            self.assertTrue( len(objects) > 0 )
            q = self.sess.query(DataObject,DataObjectMeta).\
                                            filter(DataObjectMeta.name == 'A_meta', DataObjectMeta.value <  '20').\
                                            filter(DataObjectMeta.name == 'B_meta', DataObjectMeta.value >= '20')
            self.assertTrue( len(list(q)) == len(objects) )
            q = self.sess.query(DataObject,DataObjectMeta).\
                                            filter(DataObjectMeta.name == 'B_meta').filter(DataObjectMeta.value < '28').\
                                            filter(DataObjectMeta.name == 'B_meta').filter(Like(DataObjectMeta.value, '2_'))
            self.assertTrue( len(list(q)) == len(objects)-1 )
        finally:
            for x in (objects + decoys):
                x.unlink(force=True)
            helpers.remove_unused_metadata( self.sess )

    def test_multiple_criteria_on_one_column_name(self):
        collection = self.coll_path
        filename = 'test_multiple_AVU_joins'
        file_path = '{collection}/{filename}'.format(**locals())
        objects = []
        nobj = 0
        for x in range(3,9):
            nobj += 2
            obj1 = helpers.make_object(self.sess, file_path+'-{}'.format(x))
            obj2 = helpers.make_object(self.sess, file_path+'-dummy{}'.format(x))
            objects.extend([obj1,obj2])
        self.assertTrue( nobj > 0 and len(objects) == nobj )
        q = self.sess.query(Collection,DataObject)
        dummy_test = [d for d in q if d[DataObject.name][-1:] != '8'
                                  and d[DataObject.name][-7:-1] == '-dummy' ]
        self.assertTrue( len(dummy_test) > 0 )
        q = q. filter(Like(DataObject.name, '%-dummy_')).\
               filter(Collection.name == collection) .\
               filter(DataObject.name != (filename + '-dummy8'))
        results = [r[DataObject.name] for r in q]
        self.assertTrue(len(results) == len(dummy_test))


if __name__ == '__main__':
    # let the tests find the parent irods lib
    sys.path.insert(0, os.path.abspath('../..'))
    unittest.main()
