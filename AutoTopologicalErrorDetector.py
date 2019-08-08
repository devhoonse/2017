# coding:utf-8
import arcpy
from arcpy import env
import os
import sys
import time
env.XYTolerance = '1e-003 Meters'
env.qualifiedFieldNames = False
print u"[한글 인코딩 환경]"
if "PYTHONIOENCODING" not in os.environ.keys():
    os.environ["PYTHONIOENCODING"] = u"UTF-8"
else:
    if os.environ["PYTHONIOENCODING"] != u"UTF-8":
        os.environ["PYTHONIOENCODING"] = u"UTF-8"
print u"\t[파이썬 텍스트 IO 코덱]\n\t\t>> os.environ[\"PYTHONIOENCODING\"] = %s" % os.environ["PYTHONIOENCODING"]
print u"\tsys.stdin.encoding = %s" % sys.stdin.encoding
print u"\tsys.stdout.encoding = %s" % sys.stdout.encoding
print u"\tsys.stderr.encoding = %s\n\n" % sys.stderr.encoding



def string_to_unicode(string):
    return unicode(string.decode(sys.stdin.encoding))


def joinChecker(lyr):
    flist = arcpy.Describe(lyr).fields
    for f in flist:
        if f.name.find(lyr.datasetName) > -1:
            return True
    return False


def AutoTopologyDetector_shp(shp, topology_rules=["Must Not Have Gaps (Area)", "Must Not Overlap (Area)"]):
    if os.path.basename(shp).split(u'.')[-1] == u'shp':
        print u'\n\t< %s 에 대한 토폴로지 탐지 작업을 시작합니다. >' % os.path.basename(shp)
        start_time = time.clock()
        PRJ_TM_KOREA_def = "PROJCS['TM_Korea'," \
                                    "GEOGCS['GCS_Tokyo'," \
                                                "DATUM['D_Tokyo'," \
                                                        "SPHEROID['Bessel_1841',6377397.155,299.1528128]]," \
                                                "PRIMEM['Greenwich',0.0]," \
                                                "UNIT['Degree',0.0174532925199433]]," \
                                    "PROJECTION['Transverse_Mercator']," \
                                    "PARAMETER['False_Easting',200000.0]," \
                                    "PARAMETER['False_Northing',500000.0]," \
                                    "PARAMETER['Central_Meridian',127.0028902777778]," \
                                    "PARAMETER['Scale_Factor',1.0]," \
                                    "PARAMETER['Latitude_Of_Origin',38.0]," \
                                    "UNIT['Meter',1.0]];" \
                           "-5422500 -13708100 10000;" \
                           "-100000 10000;" \
                           "-100000 10000;" \
                           "0.001;" \
                           "0.001;" \
                           "0.001;" \
                           "IsHighPrecision"
        field_mapping_def = "OriginObje \"Class 1\" true true false 255 Text 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "OriginObjectClassName,-1,-1;" \
                            "OriginOb_1 \"Feature 1\" true true false 4 Long 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "OriginObjectID,-1,-1;" \
                            "Destinatio \"Class 2\" true true false 255 Text 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "DestinationObjectClassName,-1,-1;" \
                            "Destinat_1 \"Feature 2\" true true false 4 Long 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "DestinationObjectID,-1,-1;" \
                            "RuleType \"Rule Type\" true false true 255 Text 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "RuleType,-1,-1;" \
                            "RuleDescri \"Rule Description\" true false true 255 Text 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "RuleDescription,-1,-1;" \
                            "isExceptio \"Exception\" true false true 4 Long 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "isException,-1,-1;" \
                            "Shape_Leng \"Shape_Leng\" false true true 8 Double 0 0 ," \
                                            "First," \
                                            "#," \
                                            "%s," \
                                            "Shape_Length,-1,-1"

        shp_dir = os.path.dirname(shp)
        shp_name = os.path.basename(shp).split(u'.')[0]
        GDB_name = shp_name + u'_TOPOLGDB'
        GDB_dir = os.path.join(os.path.join(shp_dir, u"ING"), u"%s" % shp_name)
        GDB_path = os.path.join(GDB_dir, GDB_name + u'.gdb')
        FDS_name = shp_name + u'_TOPOLFDS'
        FDS_path = os.path.join(GDB_path, FDS_name)
        SHP_path = os.path.join(FDS_path, shp_name)
        TOP_name = shp_name + u'_TOPOLOGY'
        TOP_path = os.path.join(FDS_path, TOP_name)
        TOPERR_name = TOP_name + u'_ERR'
        TOPERR_POL_name = TOPERR_name + u'_poly'
        TOPERR_LIN_name = TOPERR_name + u'_line'
        TOPERR_PNT_name = TOPERR_name + u'_point'
        TOPERR_POL_path = os.path.join(FDS_path, TOPERR_POL_name)
        TOPERR_LIN_path = os.path.join(FDS_path, TOPERR_LIN_name)
        TOPERR_PNT_path = os.path.join(FDS_path, TOPERR_PNT_name)
        TOPERR_shp_out_dir = os.path.join(shp_dir, u'TOPOLOGICAL_ERROR_REPORT')
        TOPERR_shp_out_path = os.path.join(TOPERR_shp_out_dir, shp_name + u'_TOPOLOGY_ERR_REPORT.shp')
        TOPERR_shp_location_out_dir = os.path.join(os.path.join(shp_dir, u'TOPOLOGICAL_ERROR_LOCATION'), u'%s' % shp_name)
        TOPERR_shp_location_POL_path = os.path.join(TOPERR_shp_location_out_dir, TOPERR_POL_name + u'.shp')
        TOPERR_shp_location_LIN_path = os.path.join(TOPERR_shp_location_out_dir, TOPERR_LIN_name + u'.shp')
        TOPERR_shp_location_PNT_path = os.path.join(TOPERR_shp_location_out_dir, TOPERR_PNT_name + u'.shp')
        TOPERR_paths = {TOPERR_POL_name: {u'유형': u'POLYGON', u'위치': TOPERR_POL_path, u'저장경로': TOPERR_shp_location_POL_path},
                        TOPERR_LIN_name: {u'유형': u'LINE',  u'위치': TOPERR_LIN_path, u'저장경로': TOPERR_shp_location_LIN_path},
                        TOPERR_PNT_name: {u'유형': u'POINT', u'위치': TOPERR_PNT_path, u'저장경로': TOPERR_shp_location_PNT_path}}
        TOPERR_REPORT_shp_fields_remainder = list(set([field.name for field in arcpy.ListFields(shp)]).union(([u'TOPOL_ERR'])))

        if not os.path.exists(GDB_dir):
            os.makedirs(GDB_dir)
        if not os.path.exists(TOPERR_shp_location_out_dir):
            os.makedirs(TOPERR_shp_location_out_dir)
        if not os.path.exists(TOPERR_shp_out_dir):
            os.makedirs(TOPERR_shp_out_dir)

        print u'\t\t(진행) 토폴로지 에러 사항 필드가 기록될 shp 파일을 복사 중입니다...'
        arcpy.Copy_management(shp, TOPERR_shp_out_path)
        print u'\t\t(완료) 토폴로지 에러 사항 필드가 기록될 shp 파일의 복사가 완료되었습니다 !'

        print u'\t\t(진행) 토폴로지 에러 사항 필드가 기록될 shp 파일을 레이어 객체로 가져오는 중입니다...'
        TOPERR_shp_out_lyr = arcpy.mapping.Layer(TOPERR_shp_out_path)
        print u'\t\t(완료) 토폴로지 에러 사항 필드가 기록될 shp 파일을 레이어 객체로 가져왔습니다 !'

        print u'\t\t(진행) 토폴로지 저장을 위한 File GDB 를 생성중입니다...'
        arcpy.CreateFileGDB_management(GDB_dir, GDB_name, "CURRENT")
        print u'\t\t(완료) 토폴로지 저장을 위한 File GDB 생성이 완료되었습니다 !'

        print u'\t\t(진행) File GDB 내에 Feature Dataset 을 생성중입니다...'
        arcpy.CreateFeatureDataset_management(GDB_path, FDS_name, PRJ_TM_KOREA_def)
        print u'\t\t(완료) File GDB 내에 Feature Dataset 생성이 완료되었습니다 !'

        print u'\t\t(진행) Feature Dataset 에 %s.shp 의 데이터를 추가중입니다...' % shp_name
        arcpy.FeatureClassToGeodatabase_conversion(shp, FDS_path)
        print u'\t\t(완료) Feature Dataset 에 %s.shp 의 데이터 추가가 완료되었습니다 !' % shp_name

        print u'\t\t(진행) Feature Dataset 에 새로운 토폴로지를 추가중입니다...'
        arcpy.CreateTopology_management(FDS_path, TOP_name, 0.001)
        print u'\t\t(완료) Feature Dataset 에 새로운 토폴로지가 추가되었습니다 !'

        print u'\t\t(진행) 생성된 Topology 에 검사할 shp 데이터를 추가중입니다...'
        arcpy.AddFeatureClassToTopology_management(TOP_path, SHP_path, "1", "1")
        print u'\t\t(완료) 생성된 Topology 에 검사할 shp 데이터를 주가하였습니다 !'


        print u'\t\t(진행) 생성된 Topology 에 검사 규칙들을 추가중입니다...'
        for topology_rule in topology_rules:
            print u'\t\t\t(진행) 생성된 Topology 에 검사규칙 %s 를 추가중입니다...' % topology_rule
            arcpy.AddRuleToTopology_management(TOP_path, topology_rule, SHP_path, "#", "#", "#")
            print u'\t\t\t(완료) 생성된 Topology 에 검사규칙 %s 를 추가하였습니다 !' % topology_rule
        print u'\t\t(완료) 생성된 Topology 에 모든 검사 규칙을 추가하였습니다 !'

        print u'\t\t(진행) 토폴로지의 에러를 탐지중입니다...'
        arcpy.ValidateTopology_management(TOP_path, "FULL_EXTENT")
        print u'\t\t(완료) 토폴로지의 에러 탐지가 완료되었습니다 !'

        print u'\t\t(진행) 토폴로지에서 탐지된 에러 사항을 저장중입니다...'
        arcpy.ExportTopologyErrors_management(TOP_path, FDS_path, TOPERR_name)
        print u'\t\t(완료) 토폴로지에서 탐지된 에러 사항 저장이 완료되었습니다 !'

        print u'\t\t(진행) 토폴로지에서 탐지된 유형별 에러 사항을 shp 파일로 저장중입니다...'
        topology_err_reports = {}
        for toperr_nm in TOPERR_paths.keys():
            print u'\t\t\t(진행) %s 유형에 대한 토폴로지 에러 사항을 shp 파일로 저장중입니다...' % TOPERR_paths[toperr_nm][u'유형']
            arcpy.FeatureClassToFeatureClass_conversion(TOPERR_paths[toperr_nm][u'위치'], TOPERR_shp_location_out_dir, toperr_nm, "#",
                                                        field_mapping_def % tuple([TOPERR_paths[toperr_nm][u'위치']
                                                                                   for i in range(8)]), "#")
            print u'\t\t\t(완료) %s 유형에 대한 토폴로지 에러 사항이 shp 파일로 저장되었습니다 !' % TOPERR_paths[toperr_nm][u'유형']

            print u'\t\t\t(진행) %s 유형에 대한 토폴로지 에러 사항을 GDB 내 %s.shp 데이터의 [%s] 필드에 기록 중입니다...' \
                  % (TOPERR_paths[toperr_nm][u'유형'], shp_name, TOPERR_paths[toperr_nm][u'유형'])
            topology_err_reports[toperr_nm] = {}
            with arcpy.da.SearchCursor(TOPERR_paths[toperr_nm][u'저장경로'], [u"OriginOb_1", u"RuleDescri"]) as cursor:
                for row in cursor:
                    if row[0] not in topology_err_reports[toperr_nm].keys():
                        topology_err_reports[toperr_nm][row[0]] = [row[1]]
                    else:
                        topology_err_reports[toperr_nm][row[0]] = list(set(topology_err_reports[toperr_nm][row[0]]).union(([row[1]])))
            for err_nm in topology_err_reports[toperr_nm].keys():
                topology_err_reports[toperr_nm][err_nm] = str(topology_err_reports[toperr_nm][err_nm]).replace(u'[', u'').replace(u']', u'').replace(u', ', u'/').replace(u'\'', u'').replace(u'\"', u'').replace(u'u', u'').replace(u'Mst', u'Must')
            if TOPERR_paths[toperr_nm][u'유형'] == u'POLYGON':
                arcpy.AddField_management(TOPERR_shp_out_path, TOPERR_paths[toperr_nm][u'유형'], "TEXT", "#", "#", "100", "#", "NULLABLE", "NON_REQUIRED", "#")
                update_cursor = arcpy.UpdateCursor(TOPERR_shp_out_path)
                for row in update_cursor:
                    if (row.getValue(u"FID") + 1) in topology_err_reports[toperr_nm].keys():
                        row.setValue(TOPERR_paths[toperr_nm][u'유형'], topology_err_reports[toperr_nm][row.getValue(u"FID") + 1])
                    update_cursor.updateRow(row)
            else:
                if TOPERR_paths[toperr_nm][u'유형'] == u'LINE':
                    with arcpy.da.SearchCursor(TOPERR_paths[toperr_nm][u'저장경로'], [u"RuleDescri"]) as cursor:
                        line_error_description = list(set([row[0] for row in cursor]).difference(([u'', u' '])))
                    for err_desc in line_error_description:
                        line_err_field_nm = u'LINE_%d' % line_error_description.index(err_desc)
                        arcpy.AddField_management(TOPERR_shp_out_path, line_err_field_nm, "TEXT", "#", "#",
                                                  "100", "#", "NULLABLE", "NON_REQUIRED", "#")
                        err_desc_select_out = os.path.join(os.path.dirname(TOPERR_paths[toperr_nm][u'저장경로']),
                                                       os.path.basename(TOPERR_paths[toperr_nm][u'저장경로']).replace(u'.shp', u'_%s.shp' % err_desc))
                        arcpy.Select_analysis(TOPERR_paths[toperr_nm][u'저장경로'], err_desc_select_out, "\"RuleDescri\" = '%s'" % err_desc)
                        err_desc_lyr = arcpy.mapping.Layer(err_desc_select_out)
                        arcpy.SelectLayerByLocation_management(in_layer=TOPERR_shp_out_lyr, overlap_type="SHARE_A_LINE_SEGMENT_WITH",
                                                               select_features=err_desc_lyr, selection_type="NEW_SELECTION")
                        arcpy.CalculateField_management(TOPERR_shp_out_lyr, line_err_field_nm, '\'%s\'' % err_desc, "PYTHON_9.3")
            print u'\t\t\t(완료) %s 유형에 대한 토폴로지 에러 사항을 GDB 내 %s.shp 데이터의 [%s] 필드에 기록하였습니다 !' % (TOPERR_paths[toperr_nm][u'유형'], shp_name, TOPERR_paths[toperr_nm][u'유형'])
        print u'\t\t(완료) 토폴로지에서 탐지된 유형별 에러 사항의 shp 파일 저장이 완료되었습니다 !'

        print u'\t\t(진행) 탐지된 토폴로지 에러 사항들을 %s 내의 각 Feature 별로 [TOPOL_ERR] 필드에 정리합니다.' % os.path.basename(TOPERR_shp_out_path)
        orig_fields = [origfield.name for origfield in arcpy.ListFields(shp)]
        err_report_field_list = [field.name for field in arcpy.ListFields(TOPERR_shp_out_path)
                                 if field.name not in orig_fields]
        arcpy.AddField_management(TOPERR_shp_out_path, u"TOPOL_ERR", "TEXT", "#", "#",
                                  "100", "#", "NULLABLE", "NON_REQUIRED", "#")
        update_cursor2 = arcpy.UpdateCursor(TOPERR_shp_out_path)
        for row in update_cursor2:
            errs_report = {fld_nm: row.getValue(fld_nm) for fld_nm in err_report_field_list}
            if len(set(errs_report.values()).difference(([u'', u' ']))) > 0:
                row.setValue(u"TOPOL_ERR",
                             str(sorted(list(set(errs_report.values()).difference(([u'', u' ']))))).replace(u',', u'/').replace(u'[', u'').replace(u']', u'').replace(u' ', u'').replace(u'\'', u'').replace(u'\"', u'').replace(u'\'', u'').replace(u'u', u'').replace(u'//', u'/').replace(u'Mst', u'Must'))
                update_cursor2.updateRow(row)
        for field in arcpy.ListFields(TOPERR_shp_out_path):
            if field.name not in TOPERR_REPORT_shp_fields_remainder:
                arcpy.DeleteField_management(TOPERR_shp_out_path, [u"%s" % field.name])
        print u'\t\t(완료) 탐지된 토폴로지 에러 사항들을 %s 내의 각 Feature 별로 [TOPOL_ERR] 필드에 정리하였습니다 !' % os.path.basename(TOPERR_shp_out_path)

        end_time = time.clock()
        print u'\t< %s 에 대한 토폴로지 탐지 작업이 모두 완료되었습니다 ! ( 소요시간 : %.4f 초 ) >' % (os.path.basename(shp), end_time - start_time)
    else:
        print u':::: ERROR ::::\n' \
              u'%s 는 shp 확장자 파일이 아닙니다. 입력하신 경로를 다시 확인해주세요 !\n' \
              u':::::::::::::::' % os.path.basename(shp)
        return None



def AutoTopologyDetector(ws):
    start_time = time.clock()
    shp_list = [os.path.join(d[0], shp) for d in os.walk(ws) for shp in d[2] if os.path.basename(shp).split(u'.')[-1] == u'shp']
    if len(shp_list) > 0:
        print u'\n[ %s ] 폴더 내에 존재하는 모든 shp 파일들에 대한 Topology Error 탐지 작업을 시작합니다.' % os.path.basename(ws)
        for shp in shp_list:
            AutoTopologyDetector_shp(shp)
        end_time = time.clock()
        print u'\n[ %s ] 폴더 내에 존재하는 모든 shp 파일들에 대한 Topology Error 탐지 작업이 완료되었습니다 ! ( 소요시간 : %.4f 초 )' % (os.path.basename(ws), end_time - start_time)
    else:
        print u'입력하신 경로 내에서 shp 파일이 검색되지 않습니다. 경로를 다시 확인해주세요 !'
        return None


dir_rawstr = raw_input(u'Directory : ')
input_dir = string_to_unicode(dir_rawstr)
if os.path.exists(input_dir):
    if os.path.isdir(input_dir):
        print u'입력하신 경로는 폴더입니다.'
        AutoTopologyDetector(input_dir)
    else:
        print u'입력하신 경로는 %s 확장자 파일입니다.' % os.path.basename(input_dir).split(u'.')[-1]
        AutoTopologyDetector_shp(input_dir)
else:
    print u'존재하지 않는 경로입니다. 경로를 다시 확인해주세요.'

