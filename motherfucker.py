# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 22:18:20 2018

@author: skywayoo
"""

import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt

box = pd.read_csv("C:/Users/skywayoo/Desktop/TEST.csv")
box['lbx'] = box['lbx']-6000
box['rtx'] = box['rtx']-6000
box['overlap'] = np.repeat("",len(box))

res = np.zeros([3000,3000])
plt.figure()
for i in range(len(box)):
    cv2.rectangle(res,(box['lbx'].values[i],box['lby'].values[i]),
                  (box['rtx'].values[i],box['rty'].values[i]),(255,0,0),1)

plt.imshow(res)

#檢查是否有重疊(顯示出重疊的index)
def check_overlap(idx,box):
    #當下的xy座標
    res=[]
    x_r = range(box['lbx'].values[idx],box['rtx'].values[idx])
    y_r = range(box['rty'].values[idx],box['lby'].values[idx])
    for i in range(len(box)):
        if i != idx:
            x_r2 = range(box['lbx'].values[i],box['rtx'].values[i])
            y_r2 = range(box['rty'].values[i],box['lby'].values[i])
            #檢查x & y
            if any(np.isin(x_r,x_r2)):
                if any(np.isin(y_r,y_r2)):
                    res.append(i)
    return res

def decide_topright(idx,idx2,box,min_dist=1):
    #當下的xy座標
    x_r = range(box['lbx'].values[idx],box['rtx'].values[idx])
    y_r = range(box['rty'].values[idx],box['lby'].values[idx])

    x_r2 = range(box['lbx'].values[idx2],box['rtx'].values[idx2])
    y_r2 = range(box['rty'].values[idx2],box['lby'].values[idx2])
    
    #判斷最右邊是否有重疊超過y一半，若有:右，無:上
    x_v = np.array(x_r)[np.isin(x_r,x_r2)]
    y_v = np.array(y_r)[np.isin(y_r,y_r2)]
    #檢查是否最右邊5個是否有重疊
    if any(np.isin(x_r[-5:],x_v)):
        #看是否有超過一半重疊 (y) 若有:往右移  無:上移
        if len(y_r)/2 < len(y_v):
            return ['R',len(x_v)+min_dist]
        else:
            return ['T',-(len(y_v)+min_dist)]
    else:
        
        return ["T",-(len(y_v)+min_dist)]

def check_left_silk(bot_comp,box):
    temp = box[box['overlap']!='X']
    idx = bot_comp.index[0]
    x_r = range(temp['lbx'].min(),temp.loc[idx]['lbx'])
    y_r = range(temp.loc[idx]['rty'],temp.loc[idx]['lby'])
    res=[]
    for i in temp.index:
        if i != bot_comp.index:
            x_r2 = range(temp.loc[i]['lbx'],temp.loc[i]['rtx'])
            y_r2 = range(temp.loc[i]['rty'],temp.loc[i]['lby'])
            #檢查x & y
            if any(np.isin(x_r,x_r2)):
                if any(np.isin(y_r,y_r2)):
                    res.append(i)       
                    
    return res

def get_topright_idx(idx,temp_box,method):
    if method=='T':
        temp = (temp_box['lby']+temp_box['rty'])/2
        now = temp.loc[idx]
        return temp[temp <= now].index        
    elif method =='R':
        temp = (temp_box['lbx']+temp_box['rtx'])/2
        now = temp.loc[idx]
        return temp[temp >= now].index    
    else:
        print ('input T or R')
        return []
            
s_val=1
for maxval in range(10000):
    record_same = 0
    if len(box) == len(box[box['overlap']=='X']):
        break
    else:
        if s_val !=0:
            s_val=s_val
        temp_box = box[box['overlap']!='X']     
        
        print(len(box[box['overlap']=='X']))
        #偵測最下面的原件
        bot_comp = temp_box[temp_box['lby'] == temp_box['lby'].max()]
            
        #判斷左邊是否有原件還沒擺
        
        if len(bot_comp)>1:  #假設有兩個同樣在最下面
        
            #挑最最左邊的 (x小的)
            bot_comp = bot_comp[bot_comp['lbx'] == bot_comp['lbx'].min()]
            bot_comp_idx = np.array(bot_comp.index)[0]
            
            if len(check_left_silk(bot_comp,box))>1:
                bot_comp = temp_box.loc[check_left_silk(bot_comp,box)]
                bot_comp = bot_comp[bot_comp['lby'] == bot_comp['lby'].max()]
            else:
                pass
            
            if len(check_overlap(bot_comp_idx,box))>0: #有重疊
                #找左下角x最小的
                over_df = box.iloc[check_overlap(np.array(bot_comp.index)[0],box)]['lbx']
                try:
                    if over_df.iloc[np.where(over_df==over_df.min())[0]].index[0] == o_idx:
                        s_val= s_val +1
                        if s_val == 2:
                            move_info = decide_topright(bot_comp_idx,o_idx,box)                
                            if move_info[0]=='T':   #所有往上移 (-y)
                                #只選中心點比他高的 (y小的)
                                for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                                        for item in ['lby','lty','rty','rby']:
                                            box.set_value(j, item, box[item].values[j]+move_info[1])
                            else:  #往右移 (+x)
                                #只選中心點比他右邊的 (X大的)
                                for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                                        for item in ['lbx','ltx','rtx','rbx']:
                                            box.set_value(j, item, box[item].values[j]+move_info[1])
                    else:
                        s_val = 0
                except:
                    pass
                o_idx = over_df.iloc[np.where(over_df==over_df.min())[0]].index[0]
                    
                move_info = decide_topright(bot_comp_idx,o_idx,box)                
                if move_info[0]=='T':   #所有往上移 (-y)
                    #只選中心點比他高的 (y小的)
                    for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                        if j != bot_comp_idx:
                            for item in ['lby','lty','rty','rby']:
                                box.set_value(j, item, box[item].values[j]+move_info[1])
                else:  #往右移 (+x)
                    #只選中心點比他右邊的 (X大的)
                    for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                        if j != bot_comp_idx:
                            for item in ['lbx','ltx','rtx','rbx']:
                                box.set_value(j, item, box[item].values[j]+move_info[1])
            else:
                box.set_value(bot_comp_idx, 'overlap', 'X')
        else:
            if len(check_left_silk(bot_comp,box))>1:
                bot_comp = temp_box.loc[check_left_silk(bot_comp,box)]
                bot_comp = bot_comp[bot_comp['lby'] == bot_comp['lby'].max()]
                #挑最最左邊的 (x小的)
                bot_comp = bot_comp[bot_comp['lbx'] == bot_comp['lbx'].min()]
            else:
                pass
            
            
            #檢查是否有重疊
            bot_comp_idx = np.array(bot_comp.index)[0]
            if len(check_overlap(bot_comp_idx,box))>0: #有重疊
                #找左下角x最小的
                over_df = box.loc[check_overlap(np.array(bot_comp.index)[0],box)]['lbx']
                try:
                    if over_df.iloc[np.where(over_df==over_df.min())[0]].index[0] == o_idx:
                        s_val= s_val +1
                        if s_val == 2:
                            move_info = decide_topright(bot_comp_idx,o_idx,box)                
                            if move_info[0]=='T':   #所有往上移 (-y)
                                #只選中心點比他高的 (y小的)
                                for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                                        for item in ['lby','lty','rty','rby']:
                                            box.set_value(j, item, box[item].values[j]+move_info[1])
                            else:  #往右移 (+x)
                                #只選中心點比他右邊的 (X大的)
                                for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                                        for item in ['lbx','ltx','rtx','rbx']:
                                            box.set_value(j, item, box[item].values[j]+move_info[1])
                    else:
                        s_val = 0
                except:
                    pass
                o_idx = over_df.iloc[np.where(over_df==over_df.min())[0]].index[0]
                
                move_info = decide_topright(bot_comp_idx,o_idx,box)
                if move_info[0]=='T':   #所有往上移 (-y)
                    #只選中心點比他高的 (y小的)
                    for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                        if j != bot_comp_idx:
                            for item in ['lby','lty','rty','rby']:
                                box.set_value(j, item, box[item].values[j]+move_info[1])
                else:  #往右移 (+x)
                    #只選中心點比他右邊的 (X大的)
                    for j in get_topright_idx(bot_comp_idx,temp_box,move_info[0]):
                        if j != bot_comp_idx:
                            for item in ['lbx','ltx','rtx','rbx']:
                                box.set_value(j, item, box[item].values[j]+move_info[1])
            else:#沒重疊
                box.set_value(bot_comp_idx, 'overlap', 'X')

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        