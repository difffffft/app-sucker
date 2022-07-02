# !/user/bin python
# -*- coding:utf-8 -*-

# pip install uiautomator2
# pip install weditor==0.6.4
# python -m weditor
# python -m uiautomator2 init
# 参考视频:https://www.bilibili.com/video/BV175411Y7JV
# 参考文档:https://blog.csdn.net/HxiongGe/article/details/116329245
import re
import os
import time
import uiautomator2 as u
import random
import threading


# textContains
# 192.168.2.101:5555
# 192.168.2.103:5555

class app:
    # 初始化工程
    def __init__(self, package_name, ip):
        self.package_name = package_name
        self.d = u.connect_adb_wifi(f"{ip}:5555")
        # self.d.settings['operation_delay'] = (0, 0)
        self.restart()

    # 重启app
    def restart(self):
        self.d.app_stop(self.package_name)
        self.d.app_start(self.package_name)


class douyin(app):
    def __init__(self):
        super().__init__("com.ss.android.ugc.aweme.lite")
        self.do_sign_in()

    # 每日签到
    def do_sign_in(self):
        self.d.xpath('//*[@resource-id="com.ss.android.ugc.aweme.lite:id/cn4"]').click()
        self.d.swipe_ext("up")
        # self.d.xpath('').click()


class kuaishou(app):
    def __init__(self, ip):
        super().__init__("com.kuaishou.nebula", ip)
        self.do_watch_ads()
        self.do_watch_video()

    # 看广告
    def do_watch_ads(self):
        self.d.xpath('//*[@text="去赚钱"]').click()
        self.d.swipe_ext("up")
        self.d.swipe_ext("up")
        try:
            self.d(textContains='恭喜你获得')
            self.d.xpath('//*[@text="首页"]').click()
            self.d.xpath('//*[@text="去赚钱"]').click()
            self.d.swipe_ext("up")
            self.d.swipe_ext("up")
        except:
            pass
        try:
            ads_task_text = self.d(textContains="看广告赚金币").get_text()
        except:
            print("广告任务已完成")
            return
        finish = re.findall(r"[\d]*/[\d]*", ads_task_text)
        if len(finish) > 0:
            complete_num, total_num = finish[0].split('/')
            complete_num = int(complete_num)
            total_num = int(total_num)
            remaining_num = total_num - complete_num
            print("剩余广告任务数量" + str(remaining_num))
            for i in range(remaining_num):
                # 模糊匹配
                self.d(textContains='看广告赚金币').click()
                try:
                    self.d(textContains='去完成任务').click()
                except:
                    pass
                while True:
                    try:
                        self.d(textContains='已成功领取奖励').click()
                        print('本次广告观看完毕')
                        break
                    except:
                        print('正在观看广告...')
            print("广告任务已完成")
        else:
            print('广告任务做完了')

    # 看视频
    def do_watch_video(self):
        self.d.xpath('//*[@text="首页"]').click()
        start = time.time()
        while True:
            end = time.time()
            print(f"观看视频已经用时:{str((end - start) / 60)}分钟")
            # 超过两小时,休息哈快手,开始薅抖音羊毛
            if (end - start) / 60 > 2 * 60:
                break
            self.d.swipe_ext("up", 0.9)
            self.do_click_like()
            self.do_click_collect()
            num = random.randint(5, 10)
            time.sleep(num)

    # 点赞(随机)
    def do_click_like(self):
        num = random.random()
        if num > 0.5:
            try:
                self.d.xpath('//*[@resource-id="com.kuaishou.nebula:id/like_icon"]').click()
            except:
                pass

    # 收藏(随机)
    def do_click_collect(self):
        num = random.random()
        if num > 0.5:
            try:
                self.d.xpath('//*[@resource-id="com.kuaishou.nebula:id/collect_icon"]').click()
            except:
                pass


def main(_user):
    os.system("adb devices")
    os.system("adb kill-server")
    os.system("adb tcpip 5555")
    kuaishou(_user['ip'])


if __name__ == '__main__':
    user_list = [
        {
            "name": "DIFFFFFFT",
            "ip": "192.168.2.101",
        },
        {
            "name": "Other",
            "ip": "192.168.2.103",
        }
    ]
    for user in user_list:
        t = threading.Thread(target=main, args=(user,))
        t.start()
