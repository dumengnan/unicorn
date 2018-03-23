1、baidu 
		检测用户名是否存在   
		https://passport.baidu.com/v2/?regnamesugg&apiver=v3&username=%E5%8F%B8%E9%A9%AC%E5%AD%94%E6%98%8E
		result：  {"errInfo":{ "no": "0" }, "data": { "userExsit": "1", "userType": "1", "suggNames": [ "鍙搁┈瀛旀槑7" , "smile鍙搁┈瀛旀槑" , "瓒呯骇鍙搁┈瀛旀槑" ] }, "traceid": ""}

		检查手机号是否存在
		https://passport.baidu.com/v2/?regphonecheck&apiver=v3&phone=18652005280&moonshad=89bc37do0110974c26594fe3578e8c712&exchange=0&isexchangeable=1&action=reg
		result：  {"errInfo":{ "no": "400005","msg": "已被其他帐号绑定","username": "司***名"},"data": {"current": "0", "accountCanCancel": "" }, "traceid": ""}


2、sina
   检测手机号是否存在
   https://login.sina.com.cn/signup/check_user.php  POST   {name:1389383223,format:json,from:mobile}
   
   检测邮箱
   https://login.sina.com.cn/signup/check_user.php  POST   {name:186243405280@126.com,format:json,from:othermail}
   
   
   
整体采用 之前的策略
但是个别定制化的内容 需要定制进行开发 
   
twitter.com
    检测手机号是否存在
       https://twitter.com/users/phone_number_available?lang=zh-cn&raw_phone_number=+8618652005280