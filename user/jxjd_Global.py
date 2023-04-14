# 引入库文件，基于telethon
from telethon import events
# 从上级目录引入 user,jdbot,chat_id变量
from .. import user, jdbot, chat_id
from ..diy.utils import read, write
import re, requests, json, asyncio

@user.on(events.NewMessage(pattern=r'^jx', outgoing=True))
async def jcmd(event):
    # 不再使用把TOKEN置入config.sh的方式，而是直接写入在py中
    # M_API_TOKEN = "91910891:ce808e74ee14191f4ac51a469186a949"
    # headers = {"token": M_API_TOKEN}
    # 赋予strText空值
    strText = ""
    # 如果当前事件是对先前消息的回复，则检索回复消息的文本，并将其传导给strText变量；如果当前事件不是对消息的回复，代码会检查是否event.raw_text可以使用空格分隔符将（事件的原始文本）拆分为两个项目的列表。如果可以，代码将获取列表的最后一项（应该是第二项）并将其分配给strText
    if event.is_reply is True:  
        reply = await event.get_reply_message()
        strText = reply.text
    else:
        msg_text = event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            strText = msg_text[-1]

    # if strText.==None:
        # await user.send_message(event.chat_id,'请指定要解析的口令,格式: j 口令 或对口令直接回复j ')
        # return
    
    # 对解析内容进行判断，如果是链接，则进行导出解析，如果是口令，先通过诺兰接口解析后导出
    # if reply.startswith("http://") or reply.startswith("https://")
    #     mgs_txt1 = reply
    #     if re.findall("/wxTeam/", mgs_txt1):
    #         msg = f'【脚本类型】 CJ组队瓜分\n`export jd_cjhy_activityId="{activateIdX[0]}"`\n`export M_WX_TEAM_URL="{urlX[0]}"`'
    #     else:
    #         msg = "【未适配变量】"
    # else:
    
    jumpUrl=""
    # Nolan 杂货铺公益API
    API = "http://api.nolanstore.top/JComExchange"
    data = {"code": strText}
    headers = {"Content-Type": "application/json"}
    issuccess=False
    for num in range(10): 
        try:
            res = requests.post(url=API,headers=headers,json=data,timeout=3)
            issuccess=True
        except:
            issuccess=False
        if issuccess:
            break
    resdata = json.loads(res.text)
    if resdata["code"]=="0":

        data = resdata["data"]
        title = data["title"]
        jumpUrl = data["jumpUrl"]
        url = re.findall("(.*?)&", jumpUrl)
        activateId = re.findall("activityId=(.*?)&", jumpUrl)
        actId = re.findall("actId=(.*?)&", jumpUrl)
        code = re.findall("code=(.*?)&", jumpUrl)
        asid = re.findall("asid=(.*)", jumpUrl)  ##锦鲤红包助力码
        shareId = re.findall("shareId=(.*)&bridgeType", jumpUrl) ## 大赢家助力码
        shareId_1 = re.findall("shareId=(.*)&source", jumpUrl) ## 京喜团圆领红包
        inviteId = re.findall("inviteId=(.*)&mpin", jumpUrl) ##炸年兽组队码
        inviteId_1 = re.findall("inviteId=(.*)&mpin", jumpUrl)  ##炸年兽助力码
        inviteId_2 = re.findall("inviteId=(.*)&mpin", jumpUrl)  ##炸年兽膨胀码
        inviteId_4 = re.findall("inviteId=(.*)&babelChannel", jumpUrl)  ## 击鼓迎春
        smp = re.findall("smp=(.*)&signhb_source", jumpUrl) ##京喜签到助力码
        inviteId_3 = re.findall("inviteId=(.*)&encryptedPin", jumpUrl)  ##城城领现金助力码
        inviter = re.findall("inviter=(.*)", jumpUrl) ## 特价版摇一摇
        inviter_1 = re.findall("inviter=(.*)&channelType", jumpUrl) ## 邀请领现金
        invite_id = re.findall("invite_id=(.*)&source", jumpUrl) ## 手机折上折
        inviterId = re.findall("inviterId=(.*)", jumpUrl) ## 特价版赚金币
        url_1 = re.findall("(https?://\S+?)&share", jumpUrl)
        url_2 = re.findall("[a-zA-z]+://[^\s]*", jumpUrl)
        ## 解析出的格式，变量是result
        result = f'【活动名称】 {data["title"]}\n【活动链接】 [点击跳转到浏览器]({data["jumpUrl"]})\n【快捷跳转】 [点击跳转到京东](https://www.yanyuwangluo.cn/jd/?url={data["jumpUrl"]})'
        
        ## CJ组队瓜分| M组队瓜分
        if re.findall("https://cjhydz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】 CJ组队瓜分\n`jd_cjhy_activityId="{activateId[0]}"`\n`M_WX_TEAM_URL="{url[0]}"`'
        
        elif re.findall("https://cjhy-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】 CJ组队瓜分\n`jd_cjhy_activityId="{activateId[0]}"`\n`M_WX_TEAM_URL="{url[0]}"`'
                
        ## LZ组队瓜分| M组队瓜分
        elif re.findall("https://lzkjdz-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】 LZ组队瓜分\n`jd_zdjr_activityId="{activateId[0]}"`\n`M_WX_TEAM_URL="{url[0]}"`'

        elif re.findall("https://lzkj-isv.isvjcloud.com/wxTeam/activity", data['jumpUrl']):
            msg = f'【脚本类型】: LZ组队瓜分\n`jd_zdjr_activityId="{activateId[0]}"`\n`M_WX_TEAM_URL="{url[0]}"`'
        
        ## 微定制瓜分
        elif re.findall("https://cjhydz-isv.isvjcloud.com/microDz/invite/activity/wx/view/index", data['jumpUrl']):
                   msg = f'【脚本类型】 微定制\n`jd_wdz_activityId="{activateId[0]}"`\n`M_WDZ_URL="{url[0]}"`'
        
        ## 微定制福袋        
        elif re.findall("https://cjhydz-isv.isvjcloud.com/microDz/invite/openLuckBag/wx/view/index", data['jumpUrl']):
                   msg = f'【脚本类型】 微定制福袋\n`jd_wdzfd_activityId="{activateId[0]}"`'                   

        ## M加购有礼
        elif re.findall("/wxCollectionActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 M加购有礼\n`M_WX_ADD_CART_URL="{url[0]}`"'

        ## M加购有礼——匹配interactsaas类型
        elif re.findall("interact(saas)?/(index)?\\?activityType=(10024)", data['jumpUrl']):
                   msg = f'【脚本类型】 M加购有礼\n`M_WX_ADD_CART_URL="{url_1[0]}`"'                   
        
        ## M幸运抽奖        
        elif re.findall("(showDrawOne|/wxPointDrawActivity/|/lzclient/|/wxDrawActivity/|^(?=.*gzsl-isv)(?=.*game).*$)", data['jumpUrl']):
                   msg = f'【脚本类型】 M幸运抽奖\n`M_WX_LUCK_DRAW_URL="{url[0]}`"'

        ## M幸运抽奖——匹配interactsaas类型        
        elif re.findall("interact(saas)?/(index)?\\?activityType=(10020|10021|10026|10031|10046|10063|10073|10080)", data['jumpUrl']):
                   msg = f'【脚本类型】 M幸运抽奖\n`M_WX_LUCK_DRAW_URL="{url_1[0]}`"'
        
        ## M关注抽奖        
        elif re.findall("/wxShopFollowActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 M关注抽奖\n`M_WX_FOLLOW_DRAW_URL="{url[0]}`"'

        ## M关注抽奖——匹配interactsaas类型         
        elif re.findall("interact(saas)?/(index)?\\?activityType=(10053|10069)", data['jumpUrl']):
                   msg = f'【脚本类型】 M关注抽奖\n`M_WX_FOLLOW_DRAW_URL="{url_1[0]}`"'
        
        ## LZ店铺游戏|M打豆豆         
        elif re.findall("/wxgame/", data['jumpUrl']):
                   msg = f'【脚本类型】 LZ店铺游戏\n`jd_wxgame_activityId="{activateId[0]}"`\n`M_WX_DADOUDOU_URL="{url[0]}"`'
        
        ## M无线游戏
        elif re.findall("/wxGameActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 M无线游戏\n`M_WX_GAME_URL="{url[0]}"`'

        ## M分享有礼
        elif re.findall("/wxShareActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 KR分享有礼\n`jd_wxShareActivity_activityId="{activateId[0]}"`\n`M_WX_SHARE_URL="{url[0]}"`'

        # elif re.findall("https://lzkjdz-isv.isvjd.com/wxShareActivity/activity", data['jumpUrl']):
            # msg = f'【脚本类型】 KR分享有礼\n`jd_wxShareActivity_activityId="{activateId[0]}"`\n`M_WX_SHARE_URL="{url[0]}"`'

        ## M读秒手速
        elif re.findall("/wxSecond/", data['jumpUrl']):
                   msg = f'【脚本类型】 读秒拼手速\n`jd_wxSecond_activityId="{activateId[0]}"`\n`M_WX_SECOND_DRAW_URL="{url[0]}"`'

        ## 知识超人
        elif re.findall("/wxKnowledgeActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 知识超人\n`jd_wxKnowledgeActivity_activityId="{activateId[0]}`"'
        # elif re.findall("https://cjhy-isv.isvjcloud.com/wxKnowledgeActivity", data['jumpUrl']):
                   # msg = f'【脚本类型】 知识超人\n`jd_wxKnowledgeActivity_activityId="{activateId[0]}`"'

        ## 大牌联合开卡
        elif re.findall("https://jinggengjcq-isv.isvjcloud.com/jdbeverage/pages", data['jumpUrl']):
                   msg = f'【脚本类型】 KR大牌联合开卡\n`DPLHTY="{actId[0]}"`'

        ## 购物车锦鲤
        elif re.findall("/wxCartKoi/", data['jumpUrl']):
                   msg = f'【脚本类型】 购物车锦鲤\n`jd_wxCartKoi_activityId="{activateId[0]}`"'

        ## M集卡抽奖
        elif re.findall("/wxCollectCard/", data['jumpUrl']):
                   msg = f'【脚本类型】 集卡抽奖\n`jd_wxCollectCard_activityId="{activateId[0]}"`\n`M_WX_COLLECT_CARD_URL="{url[0]}"`'

        ## M老虎机抽奖
        elif re.findall("/drawCenter/", data['jumpUrl']):
                   msg = f'【脚本类型】 LZ刮刮乐\n`jd_drawCenter_activityId="{activateId[0]}"`\n`M_WX_CENTER_DRAW_URL="{url[0]}"`'                   

        ## 粉丝互动
        elif re.findall("/wxFansInterActionActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 粉丝互动\n`jd_wxFansInterActionActivity_activityId="{activateId[0]}`"'

        ## 邀请赢大礼
        elif re.findall("https://prodev.m.jd.com/mall/active/dVF7gQUVKyUcuSsVhuya5d2XD4F", data['jumpUrl']):
                   msg = f'【脚本类型】 邀请赢大礼\n`yhyauthorCode="{code[0]}"`'

        ## 让福袋飞
        elif re.findall("/wxUnPackingActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 LZ让福袋飞\n`jd_wxUnPackingActivity_activityId="{activateId[0]}`"'

        ## 盖楼有礼
        elif re.findall("/wxBuildActivity/", data['jumpUrl']):
                   msg = f'【脚本类型】 盖楼有礼\n`jd_wxBuildActivity_activityId="{activateId[0]}`"'
                   
        ## M关注特效
        elif re.findall("(/wxShopGift/|shopGiftBag.html|newShopGiftBag.html)", data['jumpUrl']):
                   msg = f'【脚本类型】 店铺特效关注有礼\n`jd_wxShopGiftId="{activateId[0]}"\n`M_WX_SHOP_GIFT_URL="{url[0]}"`'

        ## 锦鲤红包
        elif re.findall("https://happy.m.jd.com/babelDiy", data['jumpUrl']):
                   msg = f'【脚本类型】 \n锦鲤红包助力码="`{asid[0]}`"'
        
        #elif re.findall("https://lzkj-isv.isvjcloud.com/prod/cc/interactsaas", data['jumpUrl']):
           # msg = f'【脚本类型】 邀请入会有礼（lzkj_loreal）\n`jd_lzkj_loreal_invite_url="{url[0]}"`'
            
        #elif re.findall("https://lorealjdcampaign-rc.isvjcloud.com/interact", data['jumpUrl']):
           # msg = f'【脚本类型】 邀请入会有礼（lzkj_loreal）\n`jd_lzkj_loreal_invite_url="{url[0]}"`'    
        
        ## 赚钱大赢家助力码
        elif re.findall("https://wqs.jd.com/sns", data['jumpUrl']):
            msg = f'【脚本类型】 赚钱大赢家助力码\n`{shareId[0]}`'
         
        ## 炸年兽
        elif re.findall("快加入我的队伍，躺赢赚红包~", data['title']):
            msg = f'【脚本类型】 炸年兽组队码\n`{inviteId[0]}`'
        elif re.findall("快快点击，助我瓜分10亿红包吧！", data['title']):
            msg = f'【脚本类型】 炸年兽助力码\n`{inviteId_1[0]}`'
        elif re.findall("帮我点一点，膨胀红包就差你的助力啦~", data['title']):
            msg = f'【脚本类型】 炸年兽膨胀码\n`{inviteId_2[0]}`'
        
        ## 京喜签到助力码
        elif re.findall("https://st.jingxi.com/sns", data['jumpUrl']):
                   msg = f'【脚本类型】 京喜签到助力码\n`{smp[0]}`'
                   
        ## 城城领现金助力码
        elif re.findall("https://bunearth.m.jd.com/babelDiy/Zeus", data['jumpUrl']):
                   msg = f'【脚本类型】 城城领现金助力码\n`{inviteId_3[0]}`'                   
        
        ## 品类联合
        elif re.findall("https://lzdz-isv.isvjcloud.com/categoryUnion/categoryUnionActivity", data['jumpUrl']):
                   msg = f'【脚本类型】 KR品类联合\n`jd_categoryUnion_activityId="{activateId[0]}`"' 
        
        ## 特价版摇一摇
        elif re.findall("https://prodev.m.jd.com/jdlite", data['jumpUrl']):
                   msg = f'【脚本类型】 特价版摇一摇\n`{inviter[0]}`'        

        ## 手机折上折
        elif re.findall("https://sjtx-dz.isvjcloud.com/phone_discount", data['jumpUrl']):
                   msg = f'【脚本类型】 手机折上折\n`{invite_id[0]}`' 
                   
        ## 特价版赚金币
        elif re.findall("https://gray.jd.com", data['jumpUrl']):
                   msg = f'【脚本类型】 特价版赚金币\n`{inviterId[0]}`'
 
        ## jd_lzkjInteract邀请有礼|邀请入会有礼（lzkj_loreal）
        elif re.findall("(interact(saas)?/(index)?\\?activityType=(10006|10070))", data['jumpUrl']):
            msg = f'【脚本类型】 jd_lzkjInteract邀请有礼\n`jd_lzkjInteractUrl="{url_1[0]}"`' 
        
        ## 加购有礼（lzkj_loreal）
        # elif re.findall("(/wxCollectionActivity/|^(?=.*lorealjdcampaign)(?=.*activityType=10024).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10024).*$)", data['jumpUrl']):
            # msg = f'【脚本类型】 M加购有礼\n`M_WX_ADD_CART_URL="{url_1[0]}"`'

        ## 关注有礼（lzkj_loreal）
        # elif re.findall("(/wxShopFollowActivity/|^(?=.*prod/cc/interactsaas)(?=.*activityType=10053).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10069).*$)", data['jumpUrl']):
            # msg = f'【脚本类型】 M关注抽奖\n`M_WX_FOLLOW_DRAW_URL="{url_1[0]}"`'

        ## 幸运抽奖（lzkj_loreal）
        # elif re.findall("(/lzclient/|/wxDrawActivity/|^(?=.*gzsl-isv)(?=.*game).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10020).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10021).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10026).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10031).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10063).*$|^(?=.*prod/cc/interactsaas)(?=.*activityType=10080).*$)", data['jumpUrl']):
            # msg = f'【脚本类型】 M幸运抽奖\n`M_WX_LUCK_DRAW_URL="{url_1[0]}"`'

        ## 邀请入会赢好礼(jinggeng)
        elif re.findall("/showInviteJoin/", data['jumpUrl']):
            msg = f'【脚本类型】 邀请入会赢好礼(jinggeng)\n`jd_showInviteJoin_activityUrl="{url_2[0]}"`'

        elif re.findall("https://lzkj-isv.isvjcloud.com/sign/sevenDay/signActivity", data['jumpUrl']):
                   msg = f'【脚本类型】 lzkj七日签到\n`LZKJ_SEVENDAY="{activateId[0]}`"'

        elif re.findall("https://lzkj-isv.isvjcloud.com/sign/signActivity2", data['jumpUrl']):
                   msg = f'【脚本类型】 lzkj签到有礼\n`LZKJ_SIGN="{activateId[0]}`"'

        elif re.findall("https://cjhy-isv.isvjcloud.com/sign/sevenDay/signActivity", data['jumpUrl']):
                   msg = f'【脚本类型】 cjhy七日签到\n`CJHY_SEVENDAY="{activateId[0]}`"'

        elif re.findall("https://cjhy-isv.isvjcloud.com/sign/signActivity", data['jumpUrl']):
                   msg = f'【脚本类型】 cjhy签到有礼\n`CJHY_SIGN="{activateId[0]}`"'

        ## 团圆领红包-2022
        elif re.findall("https://wqs.jd.com/promote/2023/spring2023", data['jumpUrl']):
                   msg = f'【脚本类型】 团圆领红包\n`{shareId_1[0]}`'

        ## 京喜团圆领红包-2023.3
        elif re.findall("https://st.jingxi.com/promote/2023/spring2023", data['jumpUrl']):
                   msg = f'【脚本类型】 京喜团圆领红包\n`{shareId_1[0]}`'                   
        
        ## 每日抢好礼
        elif re.findall("/daily/", data['jumpUrl']):
                   msg = f'【脚本类型】 每日抢好礼\n`jd_daily_activityId{activateId[0]}`'

        ## 击鼓迎春
        elif re.findall("/46nLG86c4z4z7Na48CBoC6oX3MVd/", data['jumpUrl']):
                   msg = f'【脚本类型】 击鼓迎春\n`{inviteId_4[0]}`'

        ## 邀请领现金
        elif re.findall("/2iKbfCXwhMX2SVuGDFEcKcDjbtUC/", data['jumpUrl']):
                   msg = f'【脚本类型】 邀请领现金\n`{inviter_1[0]}`'                        
        
        else:
                   msg = "【未适配变量】"
        
        # if "脚本类型" or "未适配变量" in msg:
        #     ## 最终输出内容是result+msg
        #     msg_text = await user.send_message(event.chat_id,result+"\n"+msg)
        #     ## 10秒后撤回，需要在开头导入asyncio变量
        #     await asyncio.sleep(10)
        #     await user.delete_messages(event.chat_id,msg_text)
        #     await event.delete()
    if jumpUrl != "":        
        msg_text = await user.send_message(event.chat_id,result+"\n"+msg)
        await asyncio.sleep(60)
        await user.delete_messages(event.chat_id,msg_text)
        await event.delete()
    else:
        msg_text = await user.send_message(event.chat_id,"解析出错:\n"+res.text)
        await asyncio.sleep(8)
        await user.delete_messages(event.chat_id,msg_text)
        await event.delete()

    # else:
       # await user.send_message(event.chat_id,"解析出错:"+data.get("data"))
    # except:
    #     msg = await user.send_message(event.chat_id, "口令不存在:"+data.get("data"))
    #     await asyncio.sleep(3)
    #     await user.delete_messages(event.chat_id,msg)
    #     await event.delete()
