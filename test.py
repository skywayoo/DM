import numpy as np
import pandas as pd
import re,cv2
import copy
import matplotlib.pyplot as plt

def word_position(a_r,a_idx,p_r,p_idx,m):
    if m == 'x':
        item = ['lbx','rbx']
    else:
        item = ['rty','rby']
    over_lap_info = np.isin(a_r,p_r)
    overlap_a_p = a_r[over_lap_info]
    overlap_p_p = np.where(np.isin(p_r,overlap_a_p))[0]
    overlap_mid = np.int(np.median(overlap_p_p))  
    overplap_comp_proportion = float(overlap_mid)/len(p_r)
    word_info = res.loc[p_idx][[item[0],item[1]]].values.flatten()
    word_r = np.array(range(int(word_info[0]),int(word_info[1])))
    word_overlap_x = int(np.round((len(word_r)*overplap_comp_proportion)))
    over_lap_info = np.isin(p_r,a_r)
    overlap_a_p = p_r[over_lap_info]
    overlap_p_p = np.where(np.isin(a_r,overlap_a_p))[0]
    overlap_mid = np.int(np.median(overlap_p_p))  
    overplap_comp_proportion = float(overlap_mid)/len(a_r)
    word_info = box.loc[a_idx][[item[0],item[1]]].values.flatten()
    word_r2 = np.array(range(int(word_info[0]),int(word_info[1])))
    word_overlap_x2 = int(np.round((len(word_r2)*overplap_comp_proportion)))
    return word_r[word_overlap_x]-word_r2[word_overlap_x2]


def remove_space(box):
    box_test = copy.deepcopy(box)
    x_r = range(int(box_test['lbx'].min()),int(box_test['rtx'].max()+1))
    y_r = range(int(box_test['rty'].min()),int(box_test['lby'].max()+1))
    x_all = []
    for i in range(len(box_test)):
        if i == 0:
            x_all = np.array(range(int(box_test['lbx'].values[i]),
                                   int(box_test['rtx'].values[i]+1)))
        else:
            x_all = np.append(x_all,np.array(range(int(box_test['lbx'].values[i]),
                                int(box_test['rtx'].values[i]+1))))
    x_all = x_all.flatten()
    for i in x_r:
        if np.isin(i,np.unique(x_all)):
            pass
        else:
            for j in box_test.index:
                if box_test['rbx'].values[j] < i:
                    for item in ['lbx','ltx','rbx','rtx']:
                        box_test.set_value(j, item, box_test[item].values[j]+1)
    y_all = []
    for i in range(len(box_test)):
        if i == 0:
            y_all = np.array(range(int(box_test['rty'].values[i]),
                                   int(box_test['lby'].values[i]+1)))
        else:
            y_all = np.append(y_all,np.array(range(int(box_test['rty'].values[i]),
                                                   int(box_test['lby'].values[i]+1))))
    y_all = y_all.flatten()
    for i in y_r:
        if np.isin(i,np.unique(y_all)):
            pass
        else:
            for j in box_test.index:
                if box_test['rby'].values[j] < i:
                    for item in ['lby','lty','rby','rty']:
                        box_test.set_value(j, item, box_test[item].values[j]+1)
    return box_test


def check_overlap(idx,box):
    for item in ['lbx','lby','rbx','rby','rtx','rty','ltx','lty','midx','midy']:
        box[item] = box[item].astype(int)
    res=[]
    x_r = range(box['lbx'].values[idx],box['rtx'].values[idx])
    y_r = range(box['rty'].values[idx],box['lby'].values[idx])
    for i in range(len(box)):
        if i != idx:
            x_r2 = range(box['lbx'].values[i],box['rtx'].values[i])
            y_r2 = range(box['rty'].values[i],box['lby'].values[i])
            if any(np.isin(x_r,x_r2)):
                if any(np.isin(y_r,y_r2)):
                    res.append(i)
    return res


def check_left_silk(bot_comp,box):
    temp = box
    idx = bot_comp.index[0]
    x_r = range(temp['lbx'].min(),temp.loc[idx]['lbx'])
    y_r = range(temp.loc[idx]['rty'],temp.loc[idx]['lby'])
    res=[]
    for i in temp.index:
        if i != bot_comp.index:
            x_r2 = range(temp.loc[i]['lbx'],temp.loc[i]['rtx'])
            y_r2 = range(temp.loc[i]['rty'],temp.loc[i]['lby'])
            if any(np.isin(x_r,x_r2)):
                if any(np.isin(y_r,y_r2)):
                    res.append(i)           
    return res

def check_angel(box_comp):
    box_comp_temp = copy.deepcopy(box_comp)
    for i in range(len(box_comp_temp)):
        val = box_comp_temp.iloc[i,:][['lbx','rbx']]
        x_diff = abs(val[0]-val[1])
        val = box_comp_temp.iloc[i,:][['lby','lty']]
        y_diff = abs(val[0]-val[1])
        angel = box_comp_temp['angel'].values[i]
        if x_diff>y_diff: 
            if any(angel==[0,180,360]):
                pass
            else:
                box_comp_temp.set_value(i,'angel',0)
        elif y_diff>x_diff:  
            if any(angel==[90,270]):
                pass
            else:
                box_comp_temp.set_value(i,'angel',90)
        else: 
            pass
    return box_comp_temp


def overlap_move(box_comp,box_w):
    #read file
    box_comp = pd.read_csv("box_1.csv")
    box_comp = check_angel(box_comp)
    box_w = pd.read_csv("box_1_w.csv")  
    
    for item in ['lbx','lby','rbx','rby','rtx','rty','ltx','lty','midx','midy']:
        box_comp[item] = box_comp[item].astype(int)
        box_w[item] = box_w[item].astype(int)
        
        
    unique_val_x = box_comp['lbx'].unique()
    unique_val_x = np.sort(unique_val_x)
    box_w['x_group'] = ""
    for i in range(len(box_w)):
        res = np.where(box_comp['lbx'].values[i] == unique_val_x)[0]
        box_comp.set_value(i, 'x_group', res[0])
        box_w.set_value(i, 'x_group', res[0])
    #10mil§∫¶P§@≤’
    for i in box_w['x_group'].unique():
        if len(box_w[box_w['x_group']==i]['lbx'])!=0:
            set_x = box_w[box_w['x_group']==i]['lbx'].values[0]
            for j in box_w['x_group'].unique():
                if i != j :
                    val_x = box_w[box_w['x_group']==j]['lbx'].values[0]
                    idx = box_w[box_w['x_group']==j].index
                    if (val_x >= set_x-3) & (val_x <= set_x+3):
                        for idx_val in idx:
                            box_w.set_value(idx_val, 'x_group', i)
                            box_comp.set_value(idx_val, 'x_group', i)
    unique_val_y = box_comp['lby'].unique()
    unique_val_y = -np.sort(-unique_val_y)
    box_w['y_group'] = ""
    for i in range(len(box_w)):
        res = np.where(box_comp['lby'].values[i] == unique_val_y)[0]
        box_comp.set_value(i, 'y_group', res[0])
        box_w.set_value(i, 'y_group', res[0])
    #10mil§∫¶P§@≤’
    for i in box_w['y_group'].unique():
        if len(box_w[box_w['y_group']==i]['lby'])!=0:
            set_x = box_w[box_w['y_group']==i]['lby'].values[0]
            for j in box_w['y_group'].unique():
                if i != j :
                    val_x = box_w[box_w['y_group']==j]['lby'].values[0]
                    idx = box_w[box_w['y_group']==j].index
                    if (val_x >= set_x-3) & (val_x <= set_x+3):
                        for idx_val in idx:
                            box_w.set_value(idx_val, 'y_group', i)
                            box_comp.set_value(idx_val, 'y_group', i)
    
    box = copy.deepcopy(box_w)
    box['place'] = "X"
    box_comp['place'] = "X"
    box['overlap'] = ""
    res = pd.DataFrame(columns=box.columns)
    
    #test other 
    for i in range(0,len(box)):
        if i == 0:
            temp_box = copy.deepcopy(box_comp)
            temp_box = temp_box[box_comp['place']!='O']
            temp = box_comp[box_comp['place']=='X']
            temp = temp[temp['lby'].values==temp['lby'].max()]
            temp = temp[temp['lbx'].values==temp['lbx'].min()]
            while len(check_left_silk(temp,temp_box))!=0:
                temp = box_comp.loc[check_left_silk(temp,temp_box)]
                temp = temp[temp['lby'] == temp['lby'].max()]
                temp = temp[temp['lbx'].values==temp['lbx'].min()] 
            print (i,'..',temp['comp'].values)
            box.set_value(temp.index, 'place', 'O')
            box_comp.set_value(temp.index, 'place', 'O')
            record_idx = temp.index
            res = res.append(box.loc[temp.index])
        else:
        
            temp_box = copy.deepcopy(box_comp)
            temp_box = temp_box[box_comp['place']!='O']
            temp = box_comp[box_comp['place']=='X']
            temp = temp[temp['lby'].values==temp['lby'].max()]
            temp = temp[temp['lbx'].values==temp['lbx'].min()]
            while len(check_left_silk(temp,temp_box))!=0:
                temp = box_comp.loc[check_left_silk(temp,temp_box)]
                temp = temp[temp['lby'] == temp['lby'].max()]
                temp = temp[temp['lbx'].values==temp['lbx'].min()]
            print (i,'..',temp['comp'].values)
            x_flag , y_flag = 0 , 0
            if temp['x_group'].values in res['x_group'].values:
                print ("Group: X")
                x_flag = 1
                #search x group
                x_match = res[res['x_group'].values == box.loc[temp.index]['x_group'].values]['lbx'].min()
                x_diff = box.loc[temp.index].loc[temp.index]['lbx']-x_match
                for idx in box[box['place']=='X'].index:
                    for item in ['lbx','ltx','rbx','rtx','midx']:
                        box.set_value(idx,item,box.loc[idx][item]-x_diff)
                        
            if temp['y_group'].values in res['y_group'].values:
                print ("Group: Y")
                y_flag = 1
                y_match = res[res['y_group'].values == box.loc[temp.index]['y_group'].values]['lby'].max()
                y_diff = box.loc[temp.index]['lby'].values-y_match
                for idx in box[box['place']=='X'].index:
                    for item in ['lby','lty','rby','rty','midy']:
                        box.set_value(idx,item,box.loc[idx][item]-y_diff)
                        
            if x_flag==0:
                print ("x flag == 0, 尋找對位點")
                match_res = 0
                p_l = box_comp.loc[temp.index]['lbx'].values[0]
                p_r = box_comp.loc[temp.index]['rbx'].values[0]
                match_p = box_comp.loc[res.index][['lbx','midx','rbx']]
                for j in range(len(match_p)):
                    if any(np.isin(range(p_l,p_r),range(min(match_p.iloc[j,].values),max(match_p.iloc[j,].values)))):
                        match_res=1
                        val = range(min(match_p.iloc[j,].values),max(match_p.iloc[j,].values))       
                        break
                if match_res==1:
                    p_idx = match_p.iloc[j,].name
                    a_idx = temp.index
                    a_info = box_comp.loc[a_idx][['lbx','midx','rbx']].values.flatten()
                    p_info = box_comp.loc[p_idx][['lbx','midx','rbx']].values.flatten()
                    a_r,p_r = np.array(range(a_info[0],a_info[2])),np.array(range(p_info[0],p_info[2]))
                    over_lap_info = np.isin(a_r,p_r)
                    if any(over_lap_info): #≠´≈|x
                        print ("x有找到對應的x")
                        move_b = word_position(a_r,a_idx,p_r,p_idx,'x')
                        for idx in box[box['place']=='X'].index:
                            for item in ['lbx','ltx','rbx','rtx','midx']:
                                box.set_value(idx,item,box.loc[idx][item]+move_b)
                        x_flag  = 1
                else:
                    print ("沒找到對應的x")
                    
                #檢查
            if y_flag == 0:
                print ("y flag == 0")
                match_res = 0
                p_l = box_comp.loc[temp.index]['lty'].values[0]
                p_r = box_comp.loc[temp.index]['lby'].values[0]
                match_p = box_comp.loc[res.index][['lty','midy','lby']]
                for j in range(len(match_p)):
                    if any(np.isin(range(p_l,p_r),range(min(match_p.iloc[j,].values),max(match_p.iloc[j,].values)))):
                        match_res=1
                        val = range(min(match_p.iloc[j,].values),max(match_p.iloc[j,].values))       
                        break
                if match_res==1:
                    p_idx = match_p.iloc[j,].name
                    a_idx = temp.index
                    a_info_y = box_comp.loc[a_idx][['lty','midy','lby']].values.flatten()
                    p_info_y = box_comp.loc[p_idx][['lty','midy','lby']].values.flatten()
                    a_r,p_r = np.array(range(a_info_y[0],a_info_y[2])),np.array(range(p_info_y[0],p_info_y[2]))
                    #ßP¬_A¨Oß_≠´≈|P
                    over_lap_info = np.isin(a_r,p_r)
                    if any(over_lap_info): #≠´≈|
                        move_b = word_position(a_r,a_idx,p_r,p_idx,'y')
                        #a≠Ï•Û™∫§Â¶r≠´≈|™∫§§§ﬂ¶Ï∏m°Aª›¬\©Ò¶b≠´≈|§∏•Û¶Ï∏m§§§ﬂ™∫X∂b§W
                        for idx in box[box['place']=='X'].index:
                            for item in ['lby','lty','rby','rty','midy']:
                                box.set_value(idx,item,box.loc[idx][item]+move_b)
                        y_flag=1
                        print ("找到對應的y")
                else:
                    print ("沒找到對應的y")
            
            
            #x沒對硬 y有
            if (x_flag ==0):
            
                #找出最接近lbx's元件
                min_x = 0
                df = box_comp[box_comp['rbx'] <= box_comp.loc[temp.index]['lbx'].values[0]]
                if any(np.isin(np.array(df.index),np.array(res.index))):
                    df = df.loc[res.index]
                    min_x = res.loc[df[df['rbx'] == df['rbx'].max()].head(1).index]['rbx'].values[0]
                else:
                    print ('no ref in lbx')   
                        
                #找出最接近rbx's元件
                max_x = 0
                df = box_comp[box_comp['lbx'] > box_comp.loc[temp.index]['rbx'].values[0]]
                if any(np.isin(np.array(df.index), np.array(res.index))):
                    df = df.loc[res.index]
                    max_x = res.loc[df[df['lbx'] == df['lbx'].min()].head(1).index]['lbx'].values[0]
                else:
                    
                    print ("no ref in rbx")
                
                if min_x == 0 :
                    print ('出事囉左邊沒東東')
                elif max_x == 0 :
                    print("右邊還沒有擺好的原件，往右+100擺一波，看有沒有重疊，若有在往右")
                    
                    flag = True
                    while flag:
                        for idx in box[box['place']=='X'].index:
                            for item in ['lbx','ltx','rbx','rtx','midx']:
                                box.set_value(idx,item,box.loc[idx][item]+100)
                        check_df = pd.concat([box[box['place']=='O'],box.loc[temp.index]])
                        check_df = check_df.reset_index(drop=True)
                        if len(check_overlap(len(check_df)-1,check_df))==0:
                            flag=False  
                    x_flag = 1
                else:
                    
                    print("找到左右參考範圍區間，擺放在中間 若有重疊則左點以右的全部往右移")
                    p_info = [min_x,np.int(np.mean([min_x,max_x])),max_x]
                    diff = p_info[1]-box.loc[temp.index]['midx'].values
                    for idx in box[box['place']=='X'].index:
                        for item in ['lbx','ltx','rbx','rtx','midx']:
                            box.set_value(idx,item,box.loc[idx][item]+diff)
                        
                    #檢查是否有重疊
                    check_df = pd.concat([box[box['place']=='O'],box.loc[temp.index]])
                    check_df = check_df.reset_index(drop=True)
                    if len(check_overlap(len(check_df)-1,check_df))!=0:
                        print ("重疊~~~all move right.")
                        
                        res_idx = res[res['lbx']>=p_info[0]].index
                        box_idx = box[box['place']=='X'].index
                        box_idx = np.delete(box_idx,np.where(np.isin(box_idx,temp.index))[0])
                        flag = True
                        while flag:
                            for idx in np.append(box_idx,res_idx):
                                for item in ['lbx','ltx','rbx','rtx','midx']:
                                    if idx in res_idx:
                                        res.set_value(idx,item,box.loc[idx][item]+100)
                                    else:
                                        box.set_value(idx,item,box.loc[idx][item]+100)
                            check_df = pd.concat([box[box['place']=='O'],box.loc[temp.index]])
                            check_df = check_df.reset_index(drop=True)
                            if len(check_overlap(len(check_df)-1,check_df))==0:
                                flag=False  
                        x_flag = 1
                    else:
                        print ("沒重疊")
                        
                        
            elif y_flag == 0:
                
                
                #找出最接近lby's元件(原件下面)
                max_y = 0
        
                df = box_comp[box_comp['lty'] >= box_comp.loc[temp.index]['lby'].values[0]]
                if any(np.isin(np.array(df.index),np.array(res.index))):
                    df = df.loc[res.index]
                    max_y = res.loc[df[df['lty'] == df['lty'].min()].head(1).index]['lty'].values[0]
                else:
                    print ('no ref in bot')   
                        
                #找出最接近rby's元件(原件上面)
                min_y = 0
                df = box_comp[box_comp['lby'] <= box_comp.loc[temp.index]['lty'].values[0]]
                if any(np.isin(np.array(df.index), np.array(res.index))):
                    df = df.loc[res.index]
                    min_y = res.loc[df[df['lby'] == df['lby'].max()].head(1).index]['lby'].values[0]
                else:
                    
                    print ("no ref in top")
        
                if max_y == 0 :
                    print ('出事囉下邊沒東東')
            
                elif min_y == 0 :
                    print("上面還沒有擺好的原件，往上-100擺一波，看有沒有重疊，若有在往上")
                    flag = True
                    while flag:
                        for idx in box[box['place']=='X'].index:
                            for item in ['lby','lty','rby','rty','midy']:
                                box.set_value(idx,item,box.loc[idx][item]-100)
                        check_df = pd.concat([box[box['place']=='O'],box.loc[temp.index]])
                        check_df = check_df.reset_index(drop=True)
                        if len(check_overlap(len(check_df)-1,check_df))==0:
                            flag=False  
                    x_flag = 1
                else:
                    print("找到上下參考範圍區間，擺放在中間 若有重疊則上點以上的全部往上移")
                    p_info = [min_y,np.mean([min_y,max_y]),max_y]
                    
                    #檢查是否有重疊
                    check_df = pd.concat([box[box['place']=='O'],box.loc[temp.index]])
                    check_df = check_df.reset_index(drop=True)
                    if len(check_overlap(len(check_df)-1,check_df))!=0:
                        print ("重疊~~~all move top.")
                        
                        res_idx = res[res['lby']<=p_info[0]].index
                        box_idx = box[box['place']=='X'].index
                        box_idx = np.delete(box_idx,np.where(np.isin(box_idx,temp.index))[0])
                        flag = True
                        while flag:
                            for idx in np.append(box_idx,res_idx):
                                for item in ['lby','lty','rby','rty','midy']:
                                    if idx in res_idx:
                                        res.set_value(idx,item,box.loc[idx][item]-100)
                                    else:
                                        box.set_value(idx,item,box.loc[idx][item]-100)
                            check_df = pd.concat([box[box['place']=='O'],box.loc[temp.index]])
                            check_df = check_df.reset_index(drop=True)
                            if len(check_overlap(len(check_df)-1,check_df))==0:
                                flag=False  
                        x_flag = 1
                    else:
                        print ("沒重疊")
                    
            if (x_flag == 1) and (y_flag == 1):
                print ("x,y都對齊,檢查是否有重疊")
                check_df = pd.concat([res,box.loc[temp.index]])
                check_df = check_df.reset_index(drop=True)
                
                #檢查要擺放的元件x是否有誤，須擺在對應的以外    
                
                
                if len(check_overlap(len(check_df)-1,check_df))!=0:
                    print("重疊ㄌ")
                    #檢查重疊的原因
                    #先判斷y是否重疊
                    overlap_comp = check_df.loc[check_overlap(len(check_df)-1,check_df)]
                    o_idx = box_comp[np.isin(box_comp['comp'].values,overlap_comp['comp'].values)].index
                    comp_p = box_comp.loc[o_idx][['lby','midy','lty']].dropna().head(1)
                    comp_a = box_comp.loc[temp.index][['lby','midy','lty']].dropna().head(1)
                    c_p_r = range(int(comp_p['lty'].values),int(comp_p['lby'].values))
                    c_a_r = range(int(comp_a['lty'].values),int(comp_a['lby'].values)) 
                    
                    word_p = res.loc[o_idx][['lby','midy','lty']].dropna().head(1)
                    word_a = box.loc[temp.index][['lby','midy','lty']].dropna().head(1)
                    w_p_r = range(int(word_p['lty'].values),int(word_p['lby'].values))
                    w_a_r = range(int(word_a['lty'].values),int(word_a['lby'].values)) 
                    c_over,w_over = 0,0
                    if any(np.isin(c_p_r,c_a_r)):
                        c_over = 1
                        print('元件的y重疊')
                    else:
                        print('元件的y沒重疊')
                        
                    if any(np.isin(w_p_r,w_a_r)):
                        print('文字的y重疊')
                        w_over = 1
                    else:
                        print('文字的y沒重疊')
                    
                    if (c_over == 0) and (w_over == 1):
                        print ("元件沒重疊但文字重疊 故動y往上,boty <= 該元件boty的全部往上移到沒重疊")
                        y_g_idx = res[res['y_group'] == box.loc[temp.index]['y_group'].values[0]].index
                        res_idx = np.unique(np.append(y_g_idx,res[res['lby']<=box.loc[temp.index]['lty'].values[0]].index))
                        
                        flag = True
                        while flag:
                            for idx in np.append(box[box['place']=='X'].index,res_idx):
                                for item in ['lby','lty','rby','rty','midy']:
                                    if idx in res_idx:
                                        res.set_value(idx,item,box.loc[idx][item]-100)
                                    else:
                                        box.set_value(idx,item,box.loc[idx][item]-100)
                            check_df = pd.concat([res,box.loc[temp.index]])
                            check_df = check_df.reset_index(drop=True)
                            if len(check_overlap(len(check_df)-1,check_df))==0:
                                flag=False       
                    else:
                        
                        comp_p = box_comp.loc[np.isin(box_comp['comp'].values,overlap_comp['comp'].values)][['lbx','midx','rbx']].head(1)
                        comp_a = box_comp.loc[temp.index][['lbx','midx','rbx']].head(1)
                        
                        
                        if comp_p['rbx'].values < comp_a['lbx'].values:
                            #須擺放在p的右邊，X往右移動到沒重疊
                            print ("重疊了,須擺放在p的右邊，X往右移動到沒重疊")
                            x_g_idx = res[res['x_group'] == box_comp.loc[temp.index]['x_group'].values[0]].index
                            res_idx = np.unique(np.append(x_g_idx,res[np.isin(res.index,
                                        box_comp[box_comp['rbx']<=box_comp.loc[temp.index]['lbx'].values[0]].index)].index))
                            
                            flag = True
                            while flag:
                                for idx in np.append(box[box['place']=='X'].index,res_idx):
                                    for item in ['lbx','ltx','rbx','rtx','midx']:
                                        if idx in res_idx:
                                            res.set_value(idx,item,box.loc[idx][item]+3)
                                        else:
                                            box.set_value(idx,item,box.loc[idx][item]+3)
                                check_df = pd.concat([res,box.loc[temp.index]])
                                check_df = check_df.reset_index(drop=True)
                                if len(check_overlap(len(check_df)-1,check_df))==0:
                                    flag=False       
                            
                        elif comp_p['lbx'].values > comp_a['rbx'].values:
                            #須擺放在p的左邊，X往左移動到沒重疊
                            print ("重疊了,須擺放在p的左邊，X往右移動到沒重疊")
                            x_g_idx = res[res['x_group'] == box_comp.loc[temp.index]['x_group'].values[0]].index
                            res_idx = np.unique(np.append(x_g_idx,res[np.isin(res.index,
                                        box_comp[box_comp['rbx']<=box_comp.loc[temp.index]['lbx'].values[0]].index)].index))
                            
                            flag = True
                            while flag:
                                for idx in np.append(box[box['place']=='X'].index,res_idx):
                                    for item in ['lbx','ltx','rbx','rtx','midx']:
                                        if idx in res_idx:
                                            res.set_value(idx,item,box.loc[idx][item]-3)
                                        else:
                                            box.set_value(idx,item,box.loc[idx][item]-3)
                                check_df = pd.concat([res,box.loc[temp.index]])
                                check_df = check_df.reset_index(drop=True)
                                if len(check_overlap(len(check_df)-1,check_df))==0:
                                    flag=False       
                        
                        else:
                        
                            print ("重疊了,boty <= 該元件boty的全部往上移到沒重疊")
                            y_g_idx = res[res['y_group'] == box.loc[temp.index]['y_group'].values[0]].index
                            res_idx = np.unique(np.append(y_g_idx,res[res['lby']<=box.loc[temp.index]['lty'].values[0]].index))
                            
                            flag = True
                            while flag:
                                for idx in np.append(box[box['place']=='X'].index,res_idx):
                                    for item in ['lby','lty','rby','rty','midy']:
                                        if idx in res_idx:
                                            res.set_value(idx,item,box.loc[idx][item]-100)
                                        else:
                                            box.set_value(idx,item,box.loc[idx][item]-100)
                                check_df = pd.concat([res,box.loc[temp.index]])
                                check_df = check_df.reset_index(drop=True)
                                if len(check_overlap(len(check_df)-1,check_df))==0:
                                    flag=False       
            
            box.set_value(temp.index, 'place', 'O')
            box_comp.set_value(temp.index, 'place', 'O')
            res = res.append(box.loc[temp.index])
    res = res.reset_index(drop=True)
    o_r = []
    for j in range(len(res)):
        if len(check_overlap(j,res))!=0:
            o_r.append(check_overlap(j,res))
    if len(o_r)==0:
        return res
    else:
        return False
