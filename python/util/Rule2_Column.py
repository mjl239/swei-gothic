#!/usr/bin/env python3
#encoding=utf-8

from . import spline_util
from . import Rule

# RULE # 2
# 直線，的方頭轉圓頭。
# PS: 因為 array size change, so need redo.
class Rule(Rule.Rule):
    def __init__(self):
        pass

    def apply(self, spline_dict, resume_idx, inside_stroke_dict,skip_coordinate):
        redo_travel=False
        check_first_point = False

        # allow some mistake.
        # x1,x2 的最小誤差值。
        AXIS_EQUAL_ACCURACY_MIN = 2

        # 預期是長度 400 時，可以誤差8點。
        AXIS_EQUAL_ACCURACY_RATE = 0.02

        # clone
        format_dict_array=[]
        format_dict_array = spline_dict['dots'][1:]
        format_dict_array = self.caculate_distance(format_dict_array)

        nodes_length = len(format_dict_array)
        #print("orig nodes_length:", len(spline_dict['dots']))
        #print("format nodes_length:", nodes_length)
        #print("resume_idx:", resume_idx)

        rule_need_lines = 4
        fail_code = -1
        if nodes_length >= rule_need_lines:
            for idx in range(nodes_length):
                if idx <= resume_idx:
                    # skip traveled nodes.
                    continue

                if [format_dict_array[(idx+1)%nodes_length]['x'],format_dict_array[(idx+1)%nodes_length]['y']] in skip_coordinate:
                    continue

                # 要轉換的原來的角，第3點，不能就是我們產生出來的曲線結束點。
                if [format_dict_array[(idx+2)%nodes_length]['x'],format_dict_array[(idx+2)%nodes_length]['y']] in skip_coordinate:
                    continue

                # 要轉換的原來的角，第4點，不能就是我們產生出來的曲線結束點。
                if [format_dict_array[(idx+3)%nodes_length]['x'],format_dict_array[(idx+3)%nodes_length]['y']] in skip_coordinate:
                    continue

                if [format_dict_array[idx]['x'],format_dict_array[idx]['y']] in skip_coordinate:
                    continue

                is_match_pattern = False

                #print("-"*20)
                #print(idx,"debug rule2:",format_dict_array[idx]['code'])

                #if not([format_dict_array[idx]['x'],format_dict_array[idx]['y']] in [[781,373]]):
                    #continue

                #if True:
                if False:
                    print("="*30)
                    print("index:", idx)
                    for debug_idx in range(6):
                        print(debug_idx-2,": values for rule2:",format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['code'],'-(',format_dict_array[(idx+debug_idx+nodes_length-2)%nodes_length]['distance'],')')

                # compare direction
                # start to compare.
                is_match_pattern = True

                if is_match_pattern:
                    fail_code = 100
                    is_match_pattern = False
                    if format_dict_array[(idx+1)%nodes_length]['match_stroke_width']:
                        is_match_pattern = True

                if is_match_pattern:
                    fail_code = 110
                    is_match_pattern = False
                    if format_dict_array[(idx+2)%nodes_length]['t'] == 'l':
                        is_match_pattern = True

                if is_match_pattern:
                    fail_code = 200
                    is_match_pattern = False
                
                    # 基本款
                    if format_dict_array[(idx+1)%nodes_length]['t'] == 'l':
                        if format_dict_array[(idx+0)%nodes_length]['x_equal_fuzzy']:
                            if format_dict_array[(idx+2)%nodes_length]['x_equal_fuzzy']:
                                is_match_pattern = True

                    # 追加進階款 for:.42922 「欠」系列的人頭。
                    # 線愈長，允許誤差大。
                    AXIS_EQUAL_ACCURACY = int(AXIS_EQUAL_ACCURACY_RATE * format_dict_array[(idx+1)%nodes_length]['distance'])
                    if AXIS_EQUAL_ACCURACY < AXIS_EQUAL_ACCURACY_MIN:
                        AXIS_EQUAL_ACCURACY = AXIS_EQUAL_ACCURACY_MIN

                    if format_dict_array[(idx+1)%nodes_length]['t']=='c':
                        # 中間是平的。
                        if format_dict_array[(idx+1)%nodes_length]['y_equal_fuzzy']:
                                # 另一邊切齊垂直。
                                if format_dict_array[(idx+2)%nodes_length]['x_equal_fuzzy']:
                                    # 左邊切齊
                                    if abs(format_dict_array[(idx+1)%nodes_length]['x'] - format_dict_array[(idx+1)%nodes_length]['x2']) <= AXIS_EQUAL_ACCURACY:
                                        is_match_pattern = True
                                    # 左邊切齊
                                    if abs(format_dict_array[(idx+1)%nodes_length]['x'] - format_dict_array[(idx+1)%nodes_length]['x1']) <= AXIS_EQUAL_ACCURACY:
                                        is_match_pattern = True

                # compare NEXT_DISTANCE_MIN
                if is_match_pattern:
                    fail_code = 220
                    is_match_pattern = False
                    if format_dict_array[(idx+0)%nodes_length]['distance'] > self.config.NEXT_DISTANCE_MIN:
                        is_match_pattern = True

                # compare direction
                if is_match_pattern:
                    fail_code = 400
                    #print(idx,"debug rule3:",format_dict_array[idx]['code'])
                    is_match_pattern = False
                    if format_dict_array[(idx+0)%nodes_length]['y_direction'] != format_dict_array[(idx+2)%nodes_length]['y_direction']:
                        is_match_pattern = True

                    # 不可以都同方向。
                    if format_dict_array[(idx+0)%nodes_length]['x_direction'] == -1:
                        if format_dict_array[(idx+2)%nodes_length]['x_direction'] == -1:
                            is_match_pattern = False
                    if format_dict_array[(idx+0)%nodes_length]['x_direction'] == 1:
                        if format_dict_array[(idx+2)%nodes_length]['x_direction'] == 1:
                            is_match_pattern = False

                # check from bmp file.
                if is_match_pattern:
                    is_match_pattern = False
                    fail_code = 500

                    bmp_x1 = format_dict_array[(idx+0)%nodes_length]['x']
                    bmp_y1 = format_dict_array[(idx+0)%nodes_length]['y']
                    bmp_x2 = format_dict_array[(idx+1)%nodes_length]['x']
                    bmp_y2 = format_dict_array[(idx+1)%nodes_length]['y']
                    bmp_x3 = format_dict_array[(idx+2)%nodes_length]['x']
                    bmp_y3 = format_dict_array[(idx+2)%nodes_length]['y']
                    bmp_x4 = format_dict_array[(idx+3)%nodes_length]['x']
                    bmp_y4 = format_dict_array[(idx+3)%nodes_length]['y']
                    
                    # 精簡的比對，會出錯，例如「緫」、「縃」、「繳」的方。「解」的刀。「繫」的山。
                    #bmp_x2 = bmp_x1 + (5 * format_dict_array[(idx+0)%nodes_length]['x_direction'])
                    #bmp_x3 = bmp_x4 + (5 * format_dict_array[(idx+0)%nodes_length]['x_direction'])
                    #bmp_y2 = bmp_y1 + (5 * format_dict_array[(idx+0)%nodes_length]['y_direction'])
                    #bmp_y3 = bmp_y4 + (5 * format_dict_array[(idx+0)%nodes_length]['y_direction'])
                    
                    # full rectangle compare.
                    #inside_stroke_flag = self.is_inside_stroke(bmp_x1, bmp_y1, bmp_x2, bmp_y2, bmp_x3, bmp_y3, bmp_x4, bmp_y4)

                    # compact triangle compare, 
                    # allow one coner match to continue
                    inside_stroke_flag2 = False
                    inside_stroke_flag1,inside_stroke_dict = self.test_inside_coner(bmp_x1, bmp_y1, bmp_x2, bmp_y2, bmp_x3, bmp_y3, self.config.STROKE_MIN, inside_stroke_dict)
                    if not inside_stroke_flag1:
                        # test next coner
                        inside_stroke_flag2,inside_stroke_dict = self.test_inside_coner(bmp_x2, bmp_y2, bmp_x3, bmp_y3, bmp_x4, bmp_y4, self.config.STROKE_MIN, inside_stroke_dict)

                    if inside_stroke_flag1 or inside_stroke_flag2:
                        is_match_pattern = True

                if not is_match_pattern:
                    #print(idx,"debug fail_code2:", fail_code)
                    pass

                if is_match_pattern:

                    center_x,center_y = self.apply_round_transform(format_dict_array,idx)

                    # cache transformed nodes.
                    # 加了，會造成其他的誤判，因為「點」共用。
                    #skip_coordinate.append([format_dict_array[idx]['x'],format_dict_array[idx]['y']])
                    
                    # we generated nodes
                    skip_coordinate.append([center_x,center_y])
                    
                    # next_x,y is used for next rule!
                    # 加了，會造成其他的誤判，因為「點」共用。
                    #skip_coordinate.append([new_x2,new_y2])

                    # keep the new begin point [FIX]
                    # 加了，會造成其他的誤判，因為「點」共用。例如「甾」的右上角。
                    #skip_coordinate.append([new_x1,new_y1])

                    redo_travel=True
                    check_first_point = True
                    #resume_idx = idx
                    resume_idx = -1
                    break

        if check_first_point:
            # check close path.
            self.reset_first_point(format_dict_array, spline_dict)


        return redo_travel, resume_idx, inside_stroke_dict,skip_coordinate
