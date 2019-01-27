#開始比對位置
a_idx = 24
p_idx = 22
box_word = box
def match_position(a_idx,p_idx,box_comp,box_word):
    box_comp = box
    a_info = box_comp.loc[a_idx][['lbx','midx','rbx']].values
    p_info = box_comp.loc[p_idx][['lbx','midx','rbx']].values
    a_r,p_r = np.array(range(a_info[0],a_info[2])),np.array(range(p_info[0],p_info[2]))
    
    #判斷A是否重疊P
    over_lap_info = np.isin(a_r,p_r)
    if any(over_lap_info): #重疊
        #看P哪些重疊
        overlap_a_p = a_r[over_lap_info]
        #P重疊X在序列中的位置
        overlap_p_p = np.where(np.isin(p_r,overlap_a_p))[0]
        overlap_mid = np.int(np.median(overlap_p_p))   
        overplap_comp_proportion = overlap_mid/len(p_r)        
        word_info = box_word.loc[p_idx][['lbx','rbx']].values
        word_r = np.array(range(word_info[0],word_info[1]))
        #取得文字部份的重疊位置
        word_overlap_x = int(len(word_r)*overplap_comp_proportion)
        #a原件的文字中心點需擺放在這的X軸上
        word_r[word_overlap_x]
    else: #X軸沒重疊
        #判斷原件在左邊還右邊
        if a_info[1] > p_info[1]:
            #A在P右邊
            #A的左下角X不能小於P的右下角
            a_info[0] > p_info[1]        
        else:
            #A在P左邊
            #A的左下角X不能小於P的右下角
            a_info[1] < p_info[0] 
