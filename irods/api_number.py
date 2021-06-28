api_number = {
    # 500 - 599 - Internal File I/O API calls
    "FILE_CREATE_AN": 500,
    "FILE_OPEN_AN": 501,
    "FILE_WRITE_AN": 502,
    "FILE_CLOSE_AN": 503,
    "FILE_LSEEK_AN": 504,
    "FILE_READ_AN": 505,
    "FILE_UNLINK_AN": 506,
    "FILE_MKDIR_AN": 507,
    "FILE_CHMOD_AN": 508,
    "FILE_RMDIR_AN": 509,
    "FILE_STAT_AN": 510,
    "FILE_FSTAT_AN": 511,
    "FILE_FSYNC_AN": 512,
    "FILE_STAGE_AN": 513,
    "FILE_GET_FS_FREE_SPACE_AN": 514,
    "FILE_OPENDIR_AN": 515,
    "FILE_CLOSEDIR_AN": 516,
    "FILE_READDIR_AN": 517,
    "FILE_PUT_AN": 518,
    "FILE_GET_AN": 519,
    "FILE_CHKSUM_AN": 520,
    "CHK_N_V_PATH_PERM_AN": 521,
    "FILE_RENAME_AN": 522,
    "FILE_TRUNCATE_AN": 523,
    "FILE_STAGE_TO_CACHE_AN": 524,
    "FILE_SYNC_TO_ARCH_AN": 525,

    # 600 - 699 - Object File I/O API calls
    "DATA_OBJ_CREATE_AN": 601,
    "DATA_OBJ_OPEN_AN": 602,
    "DATA_OBJ_PUT_AN": 606,
    "DATA_PUT_AN": 607,
    "DATA_OBJ_GET_AN": 608,
    "DATA_GET_AN": 609,
    "DATA_OBJ_REPL250_AN": 610,
    "DATA_COPY_AN": 611,
    "DATA_OBJ_COPY250_AN": 613,
    "SIMPLE_QUERY_AN": 614,
    "DATA_OBJ_UNLINK_AN": 615,
    "REG_DATA_OBJ_AN": 619,
    "UNREG_DATA_OBJ_AN": 620,
    "REG_REPLICA_AN": 621,
    "MOD_DATA_OBJ_META_AN": 622,
    "RULE_EXEC_SUBMIT_AN": 623,
    "RULE_EXEC_DEL_AN": 624,
    "EXEC_MY_RULE_AN": 625,
    "OPR_COMPLETE_AN": 626,
    "DATA_OBJ_RENAME_AN": 627,
    "DATA_OBJ_RSYNC_AN": 628,
    "DATA_OBJ_CHKSUM_AN": 629,
    "PHY_PATH_REG_AN": 630,
    "DATA_OBJ_PHYMV250_AN": 631,
    "DATA_OBJ_TRIM_AN": 632,
    "OBJ_STAT_AN": 633,
    "SUB_STRUCT_FILE_CREATE_AN": 635,
    "SUB_STRUCT_FILE_OPEN_AN": 636,
    "SUB_STRUCT_FILE_READ_AN": 637,
    "SUB_STRUCT_FILE_WRITE_AN": 638,
    "SUB_STRUCT_FILE_CLOSE_AN": 639,
    "SUB_STRUCT_FILE_UNLINK_AN": 640,
    "SUB_STRUCT_FILE_STAT_AN": 641,
    "SUB_STRUCT_FILE_FSTAT_AN": 642,
    "SUB_STRUCT_FILE_LSEEK_AN": 643,
    "SUB_STRUCT_FILE_RENAME_AN": 644,
    "QUERY_SPEC_COLL_AN": 645,
    "SUB_STRUCT_FILE_MKDIR_AN": 647,
    "SUB_STRUCT_FILE_RMDIR_AN": 648,
    "SUB_STRUCT_FILE_OPENDIR_AN": 649,
    "SUB_STRUCT_FILE_READDIR_AN": 650,
    "SUB_STRUCT_FILE_CLOSEDIR_AN": 651,
    "DATA_OBJ_TRUNCATE_AN": 652,
    "SUB_STRUCT_FILE_TRUNCATE_AN": 653,
    "GET_XMSG_TICKET_AN": 654,
    "SEND_XMSG_AN": 655,
    "RCV_XMSG_AN": 656,
    "SUB_STRUCT_FILE_GET_AN": 657,
    "SUB_STRUCT_FILE_PUT_AN": 658,
    "SYNC_MOUNTED_COLL_AN": 659,
    "STRUCT_FILE_SYNC_AN": 660,
    "CLOSE_COLLECTION_AN": 661,
    "STRUCT_FILE_EXTRACT_AN": 664,
    "STRUCT_FILE_EXT_AND_REG_AN": 665,
    "STRUCT_FILE_BUNDLE_AN": 666,
    "CHK_OBJ_PERM_AND_STAT_AN": 667,
    "GET_REMOTE_ZONE_RESC_AN": 668,
    "DATA_OBJ_OPEN_AND_STAT_AN": 669,
    "L3_FILE_GET_SINGLE_BUF_AN": 670,
    "L3_FILE_PUT_SINGLE_BUF_AN": 671,
    "DATA_OBJ_CREATE_AND_STAT_AN": 672,
    "DATA_OBJ_CLOSE_AN": 673,
    "DATA_OBJ_LSEEK_AN": 674,
    "DATA_OBJ_READ_AN": 675,
    "DATA_OBJ_WRITE_AN": 676,
    "COLL_REPL_AN": 677,
    "OPEN_COLLECTION_AN": 678,
    "RM_COLL_AN": 679,
    "MOD_COLL_AN": 680,
    "COLL_CREATE_AN": 681,
    "RM_COLL_OLD_AN": 682,
    "REG_COLL_AN": 683,
    "PHY_BUNDLE_COLL_AN": 684,
    "UNBUN_AND_REG_PHY_BUNFILE_AN": 685,
    "GET_HOST_FOR_PUT_AN": 686,
    "GET_RESC_QUOTA_AN": 687,
    "BULK_DATA_OBJ_REG_AN": 688,
    "BULK_DATA_OBJ_PUT_AN": 689,
    "PROC_STAT_AN": 690,
    "STREAM_READ_AN": 691,
    "EXEC_CMD_AN": 692,
    "STREAM_CLOSE_AN": 693,
    "GET_HOST_FOR_GET_AN": 694,
    "DATA_OBJ_REPL_AN": 695,
    "DATA_OBJ_COPY_AN": 696,
    "DATA_OBJ_PHYMV_AN": 697,
    "DATA_OBJ_FSYNC_AN": 698,
    "DATA_OBJ_LOCK_AN": 699,

    # 700 - 799 - Metadata API calls
    "GET_MISC_SVR_INFO_AN": 700,
    "GENERAL_ADMIN_AN": 701,
    "GEN_QUERY_AN": 702,
    "AUTH_REQUEST_AN": 703,
    "AUTH_RESPONSE_AN": 704,
    "AUTH_CHECK_AN": 705,
    "MOD_AVU_METADATA_AN": 706,
    "MOD_ACCESS_CONTROL_AN": 707,
    "RULE_EXEC_MOD_AN": 708,
    "GET_TEMP_PASSWORD_AN": 709,
    "GENERAL_UPDATE_AN": 710,
    "GSI_AUTH_REQUEST_AN": 711,
    "READ_COLLECTION_AN": 713,
    "USER_ADMIN_AN": 714,
    "GENERAL_ROW_INSERT_AN": 715,
    "GENERAL_ROW_PURGE_AN": 716,
    "KRB_AUTH_REQUEST_AN": 717,
    "END_TRANSACTION_AN": 718,
    "DATABASE_RESC_OPEN_AN": 719,
    "DATABASE_OBJ_CONTROL_AN": 720,
    "DATABASE_RESC_CLOSE_AN": 721,
    "SPECIFIC_QUERY_AN": 722,
    "TICKET_ADMIN_AN": 723,
    "GET_TEMP_PASSWORD_FOR_OTHER_AN": 724,
    "PAM_AUTH_REQUEST_AN": 725,

    "EXEC_CMD241_AN": 634,

    "DATA_OBJ_READ201_AN": 603,
    "DATA_OBJ_WRITE201_AN": 604,
    "DATA_OBJ_CLOSE201_AN": 605,
    "DATA_OBJ_LSEEK201_AN": 612,
    "RM_COLL_OLD201_AN": 617,
    "REG_COLL201_AN": 618,
    "MOD_COLL201_AN": 646,
    "COLL_REPL201_AN": 662,
    "RM_COLL201_AN": 663,
    "OPEN_COLLECTION201_AN": 712,

    # 1000 - 1059 - NETCDF API calls
    "NC_OPEN_AN": 1000,
    "NC_CREATE_AN": 1001,
    "NC_CLOSE_AN": 1002,
    "NC_INQ_ID_AN": 1003,
    "NC_INQ_WITH_ID_AN": 1004,
    "NC_GET_VARS_BY_TYPE_AN": 1005,
    "NCCF_GET_VARA_AN": 1006,
    "NC_INQ_AN": 1007,
    "NC_OPEN_GROUP_AN": 1008,
    "NC_INQ_GRPS_AN": 1009,
    "NC_REG_GLOBAL_ATTR_AN": 1010,

    # 1060 - 1099 - OOI API calls
    "OOI_GEN_SERV_REQ_AN": 1060,

    # 1100 - 1200 - SSL API calls
    "SSL_START_AN": 1100,
    "SSL_END_AN": 1101,
    "ATOMIC_APPLY_METADATA_OPERATIONS_APN": 20002,
    "GET_FILE_DESCRIPTOR_INFO_APN": 20000,
    "REPLICA_CLOSE_APN": 20004
}
