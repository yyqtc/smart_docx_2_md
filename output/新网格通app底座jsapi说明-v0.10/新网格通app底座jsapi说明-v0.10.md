# 广东移动新网格通app底座JSAPI说明

**版本：V0.10**

**日期：2025年04月**

---

## 概述

### 文档说明
本文档定义新网格通app底座上的WebView容器加载的H5页面可以使用的JSAPI，该JSAPI用于H5页面调用新网格通底座提供的原生能力。

### 接入方式
app加载网页完成后会注入`ado`对象，H5页面可以监听`adoInit`事件，然后使用`window.ado`对象调用JSAPI。

#### 监听adoInit事件代码
```javascript
connectAdo(callback) {
  if (window.ado) {
    callback();
  } else {
    document.addEventListener('adoInit', function () {
      console.log('testado init adoInitSuccess event');
      callback();
    }, false);
  }
}

connectAdo(() => {
  console.log('ado中的方法列表：');
  window.ado.xx;
});
```

#### JSAPI调用示例
```javascript
let params = {
  url: 'https://www.baidu.com',
  h5AuthType: '9',
  isKeyFunc: '1'
};

window.ado.openUrl(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

### 统一参数说明

#### 输出格式
```json
{
  "code": 1,
  "message": "错误信息",
  "data": 返回值
}
```

#### 返回编码code说明
- `1`: 成功
- 其他: 错误码（具体见各接口说明）

---

## 修订记录

（文档中未提供具体内容）

---

## 接口说明

### 基础功能

#### 2.1.1 单点登录(SSO)(获取临时token)

- **方法名称**: `singleSignOn`
- **适用范围**: 页面浏览器

##### 参数说明
- `appId`: 应用ID

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": {
    "token": "eyJRlc3QiLCJjb250ZW50IjoiYlFNYZFVhOHifQ=="
  }
}
```

##### 示例
```javascript
window.ado.singleSignOn({
  appId: '400000'
}).then((res) => {
  let data = res.data;
  if (data) {
    let token = data.token;
  }
}).catch(function (err) {
  console.log(err);
});
```

#### 2.1.2 第三方登录

- **方法名称**: `thirdLogin`
- **适用范围**: 页面浏览器

##### 参数说明
- `appId`: 平台分配的应用标识符
- `ssoTicket`: 第三方accessToken

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": null
}
```

##### 示例
```javascript
let params = {
  appId: '平台分配的应用标识符',
  ssoTicket: '第三方accessToken'
};

window.ado.thirdLogin(params)
  .then((res) => {
    console.log(res);
  })
  .catch(function (err) {
    console.log(err);
  });
```

#### 2.1.3 打开app底座的小程序、网格通应用、h5网页

- **方法名称**: `openUrl`
- **适用范围**: 页面浏览器

##### 参数说明
- `url`: 目标URL
- `h5AuthType`: H5认证类型
- `isKeyFunc`: 是否为核心功能

##### 返回值data说明
调用是否成功
```json
{
  "code": 1,
  "message": "success",
  "data": null
}
```

##### 示例
```javascript
let params = {
  url: 'https://www.baidu.com',
  h5AuthType: '9',
  isKeyFunc: '1'
};

window.ado.openUrl(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 2.1.4 监听拦截物理返回键（安卓）

- **方法名称**: `backEventListener`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 参数说明
- `isInterceptBackPress`: 是否拦截返回键

##### 返回值data说明
```json
{
  "code": 1018,
  "message": "success",
  "data": null
}
```

##### 示例
```javascript
let isInterceptBackPress = true;
window.ado.backEventListener(isInterceptBackPress)
  .then(function (res) {
    console.log('点击了物理返回键');
    // 监听物理返回键，进行对应操作
    // todo
  })
  .catch(function (err) {
    console.log(err);
  });
```

#### 2.1.5 检测权限

- **方法名称**: `checkPermission`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 参数说明
- `id`: 权限ID
- `permissionCode`: 权限代码
- `permissionDescription`: 权限描述

##### 返回值data说明
```json
{
  "code": 1,
  "message": "出错内容，此内容仅用于记录日志",
  "data": true,  // true（有权）/ false（无权）
  "checkOnly": false  // true: 已经授权，false：弹出了授权弹框
}
```

##### 示例
```javascript
let params = {
  id: 'getLocation',
  permissionCode: 'LOCATION',
  permissionDescription: '需要使用位置权限获取位置信息'
};

window.ado.checkPermission(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

### 界面操作

#### 2.2.1 新建一个浏览器页面打开指定的URL

- **方法名称**: `open`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 参数说明
支持两种调用方式：

1. 直接传参
   - `url`: URL地址
   - `showTitle`: 是否显示标题栏
   - `title`: 页面标题
   - `orientation`: 屏幕方向

2. 传入参数对象
   - `params`: 包含上述参数及额外请求头等配置

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": null
}
```

##### 示例
```javascript
// 示例1
let url = 'https://www.baidu.com';
let showTitle = true;
let title = '打开页面的标题';
let orientation = 'portrait';
window.ado.open(url, showTitle, title, orientation);

// 示例3
let params = {
  url: 'https://www.baidu.com',
  showTitle: true,
  title: '打开页面的标题',
  orientation: 'portrait',
  header: {
    headerKey1: '我要传的请求头值1',
    headerKey2: '我要传的请求头值2'
  }
};
window.ado.open(params);
```

#### 2.2.2 关闭当前浏览器

- **方法名称**: `close`
- **适用范围**: 工作台项浏览器，页面浏览器

##### 参数说明
无

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": null
}
```

##### 示例
```javascript
window.ado.close();
```

### 位置服务

#### 取得经纬度

- **方法名称**: `getLatLng`
- **适用范围**: 页面浏览器

##### 参数说明
- `timeout`: 超时时间
- `loop`: 是否循环获取
- `permissionId`: 权限ID
- `permissionDescription`: 权限描述

##### 返回值data说明
```json
{
  "code": 1,     // 成功
  // 9001: 未开启权限
  // 9002: 未开启定位
  // 9003: 未取到定位数据
  "message": "出错内容，此内容仅用于记录日志",
  "data": {
    "pre": {
      "lat": 22.960679758736962,
      "lng": 113.88831695369365,
      "time": 1635925700435
    },
    "cur": {
      "lat": 22.960679758736962,
      "lng": 113.88831695369365,
      "time": 1635925700435
    }
  }
}
```

##### 示例
```javascript
let params = {
  timeout: 3000,
  loop: false,
  permissionId: 'getLatLng_1',
  permissionDescription: '因xx功能，需要获取定位权限'
};

window.ado.getLatLng(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 持续获取经纬度

- **方法名称**: `getLatLngLoop`
- **适用范围**: 页面浏览器

> 参数与返回值同`getLatLng`，持续获取模式

##### 示例
```javascript
// 同getLatLng调用方式
window.ado.getLatLng(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

### 图片操作

#### 2.4.1 下载图片

- **方法名称**: `downImage`
- **适用范围**: 页面浏览器

##### 参数说明
- `url`: 图片URL
- `permissionId`: 权限ID
- `permissionDescription`: 权限描述

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": "图片路径"
}
```

##### 示例
```javascript
let params = {
  url: '要下载图片的url',
  permissionId: 'downImage_1',
  permissionDescription: '因xx功能，需要获取文件存储权限'
};

window.ado.downImage(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 2.4.2 从相册选择相片

- **方法名称**: `selectImageFromAlbum`
- **适用范围**: 页面浏览器

##### 参数说明
- `maxNumber`: 最大选择数量
- `maxWidth`: 最大宽度
- `maxHeight`: 最大高度
- `quality`: 图像质量
- `callbackType`: 回调类型（2: base64, 3: 文件路径）

##### 返回值data说明
**callbackType=2 时：**
```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "size": "相片大小",
      "base64": "文件base64字符串",
      "fileName": "文件名称",
      "extension": "文件扩展名"
    }
  ]
}
```

**callbackType=3 时：**
```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "size": "相片大小",
      "filePath": "文件本地路径",
      "fileName": "文件名称",
      "extension": "文件扩展名"
    }
  ]
}
```

##### 示例
```javascript
// 示例1
let params = {
  maxNumber: 1,
  maxWidth: 1000,
  maxHeight: 1000,
  quality: 85,
  showProgress: true,
  callbackType: 2,
  appId: '',
  requestUrl: '',
  requestHeaders: {},
  permissionId: 'selectImageFromAlbum_1',
  permissionDescription: '因xx功能，需要获取相册权限',
  cut: false
};

window.ado.selectImageFromAlbum(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });

// 示例2
let params = {
  maxWidth: 1000,
  maxHeight: 1000,
  callbackType: 3,
  permissionId: 'selectImageFromAlbum_1',
  permissionDescription: '因xx功能，需要获取相册权限'
};

window.ado.selectImageFromAlbum(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 2.4.3 从文件夹取得相片

- **方法名称**: `getImage`
- **适用范围**: 页面浏览器

##### 参数说明
- `folderName`: 相册文件夹名称
- `imageName`: 图片名称
- `width`: 缩略图宽度
- `height`: 缩略图高度

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "path": "相片地址",
      "base64": "base64缩略图字符串"
    }
  ]
}
```

##### 示例
```javascript
let params = {
  folderName: '相册文件夹名称',
  imageName: '图片名称',
  width: 50,
  height: 50
};

window.ado.getImage(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

### 文件操作

#### 打开文件

- **方法名称**: `systemOpenFile`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "data": "/storage/emulated/0/Android/data/com.huawei.nis.android.gridbee.vt3/cache/bc5dc8c4-841f-4624-9af6-253bede3aa8a?appId=49a8119e-8e1f-47c8-9b05-585f11e81b36",
  "message": ""
}
```

##### 示例
```javascript
let url = '要打开的文件路径';
window.ado.systemOpenFile(url)
  .then((res) => {
    console.log(res);
  })
  .catch(error => {
    console.log(error);
  });
```

#### 下载文件

- **方法名称**: `downFile`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 参数说明
- `url`: 文件URL
- `config`: 配置对象（含请求头、请求体、方法）

> 特殊说明：使用`requestHeader`、`requestBody`、`requestMethod`暂不支持非同域的https请求

##### 返回值data说明
```json
{
  "code": 1,
  "data": "/storage/emulated/0/Android/data/com.huawei.nis.android.gridbee.vt3/cache/bc5dc8c4-841f-4624-9af6-253bede3aa8a?appId=49a8119e-8e1f-47c8-9b05-585f11e81b36",
  "message": ""
}
```

##### 示例
```javascript
let url = 'http://a/b/c.txt';
let config = {
  requestHeader: {
    headerKey1: '我要传的请求头值1',
    headerKey2: '我要传的请求头值2'
  },
  requestBody: {
    bodyKey1: '我要传的请求体值1',
    bodyKey2: '我要传的请求体值2'
  },
  requestMethod: 'post'
};

window.ado.downFile(url, config)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 选择本地文件

- **方法名称**: `selectLocalFiles`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "filePath": "/root/file/介绍文档.docx"
    }
  ]
}
```

##### 示例
```javascript
let object = {
  fileNumber: 1,
  type: ['docx','xlsx', 'jpg', 'png'],
  selectType: 'file'
};

window.ado.selectLocalFiles(object)
  .then(function (res) {
    let data = res.data;
  })
  .catch(function (err) {
    console.log(err);
  });
```

#### 上传本地文件

- **方法名称**: `uploadLocalFiles`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 返回值data说明
当传入`requestUrl`时：
```json
{
  "code": 1,
  "message": "success",
  "data": {
    "/root/file/介绍文档.docx": "对应文件上传接口返回的数据",
    "/root/file/演讲文档.docx": "对应文件上传接口返回的数据"
  }
}
```

##### 示例
```javascript
let object = {
  filePathList: [
    '../files/测试文档1.docx',
    '../files/测试文档2.docx'
  ],
  requestUrl: '上传指定的url',
  requestHeaders: {},
  requestParams: {}
};

window.ado.uploadLocalFiles(params)
  .then(function (res) {
    console.log(res.data);
  })
  .catch(function (err) {
    console.log(err);
  });
```

#### 打开PDF

- **方法名称**: `openPDF`
- **适用范围**: tabbar浏览器，工作台项浏览器，页面浏览器

##### 参数说明
- `filePath`: PDF文件路径
- `title`: 页面标题
- `config`: 请求配置（可选）

> 特殊说明：使用`requestHeader`、`requestBody`、`requestMethod`暂不支持非同域的https请求

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": null
}
```

##### 示例
```javascript
// 示例1：不使用请求配置
let params = {
  filePath: 'http://abc/download/file/previewFile.pdf',
  title: '页面标题'
};

window.ado.openPDF(params)
  .then(function (res) {
    console.log(res);
  })
  .catch(function (err) {
    console.log(err);
  });

// 示例2：使用请求配置
let object = {
  filePath: 'http://abc/download/file/previewFile.pdf',
  title: '页面标题',
  config: {
    requestHeader: {},
    requestBody: {},
    requestMethod: 'post'
  }
};

window.ado.openPDF(params)
  .then(function (res) {
    console.log(res);
  })
  .catch(function (err) {
    console.log(err);
  });
```

### 设备功能

#### 2.5.1 调用系统相机进行拍照

- **方法名称**: `selectImageFromSystemCamera`
- **适用范围**: 页面浏览器

##### 返回值data说明
**callbackType=2 时：**
```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "size": "相片大小",
      "base64": "文件base64字符串",
      "fileName": "文件名称",
      "extension": "文件扩展名"
    }
  ]
}
```

**callbackType=3 时：**
```json
{
  "code": 1,
  "message": "success",
  "data": [
    {
      "size": "相片大小",
      "filePath": "文件本地路径",
      "fileName": "文件名称",
      "extension": "文件扩展名"
    }
  ]
}
```

##### 示例
```javascript
let params = {
  maxNumber: 1,
  maxWidth: 1000,
  maxHeight: 1000,
  quality: 85,
  showProgress: true,
  callbackType: 2,
  permissionId: 'selectImageFromSystemCamera_1',
  permissionDescription: '因xx功能，需要获取相机权限',
  cut: false
};

window.ado.selectImageFromSystemCamera(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 2.5.2 调用自定义相机进行拍照

- **方法名称**: `selectImageFromCustomCamera`
- **适用范围**: 页面浏览器

> 参数与返回值同`selectImageFromSystemCamera`

##### 示例
```javascript
// 调用方式相同
window.ado.selectImageFromSystemCamera(params)
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

#### 2.5.3 调用扫一扫

- **方法名称**: `scanCode`
- **适用范围**: 页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success",
  "data": "扫描内容"
}
```

##### 示例
```javascript
let permissionId = 'scanCode_1';
let permissionDescription = '因xx功能，需要获取相机权限';

window.ado.scanCode({
  permissionId,
  permissionDescription
})
  .then((res) => {
    let data = res.data;
  })
  .catch(error => {
    console.log(error);
  });
```

### 语音识别

#### 开始语音识别

- **方法名称**: `startVoiceRecord`
- **适用范围**: 页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.startVoiceRecord()
  .then((res) => {
    console.log('startVoiceRecord res = ' + JSON.stringify(res));
  })
  .catch(error => {
    console.log(error);
  });
```

#### 结束语音识别

- **方法名称**: `stopVoiceRecord`
- **适用范围**: 页面浏览器

##### 参数说明
无

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.stopVoiceRecord()
  .then((res) => {
    console.log('stopVoiceRecord');
  })
  .catch(error => {
    console.log(error);
  });
```

#### 监听语音识别结果

```javascript
connectAdo(callback) {
  if (window.ado) {
    callback();
  } else {
    document.addEventListener('adoInit', function () {
      console.log('testado init adoInitSuccess event');
      callback();
    }, false);
  }
},

// 监听语音识别结果事件
mounted() {
  this.connectAdo(() => {
    window.ado.subscribe('voiceRecordEvent', (res) => {
      console.log('handle voiceRecordEvent ', JSON.stringify(res));
      if (res.type === 'message') {
        this.voiceResult = res.message;
      }
    });
  });
},

// 取消监听
unMounted() {
  this.connectAdo(() => {
    window.ado.unSubscribe('voiceRecordEvent');
  });
},
```

### 录音

#### 开始录音录制

- **方法名称**: `startRecording`
- **适用范围**: 页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.startRecording()
  .then((res) => {
    console.log('startVoiceRecord res = ' + JSON.stringify(res));
  })
  .catch(error => {
    console.log(error);
  });
```

#### 结束录音

- **方法名称**: `stopRecording`
- **适用范围**: 页面浏览器

##### 参数说明
无

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.stopRecording()
  .then((res) => {
    console.log('stopVoiceRecord');
  })
  .catch(error => {
    console.log(error);
  });
```

#### 监听录音结果

```javascript
connectAdo(callback) {
  if (window.ado) {
    callback();
  } else {
    document.addEventListener('adoInit', function () {
      callback();
    }, false);
  }
},

// 监听语音识别结果事件
mounted() {
  this.connectAdo(() => {
    window.ado.subscribe('voiceRecordEvent', (res) => {
      console.log('handle voiceRecordEvent ', JSON.stringify(res));
      if (res.type === 'pcm') {
        this.voiceResult = res.message;
      }
    });
  });
},

// 取消监听
unMounted() {
  this.connectAdo(() => {
    window.ado.unSubscribe('voiceRecordEvent');
  });
},
```

### 悬浮图标

#### 设置悬浮图标

- **方法名称**: `showFloatMenu`
- **适用范围**: 页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.showFloatMenu({
  "ImageUrl": "xx",
  "floatTextList": "XX"
})
  .then((res) => {
  })
  .catch(error => {
    console.log(error);
  });
```

#### 隐藏悬浮图标

- **方法名称**: `hideFloatMenu`
- **适用范围**: 页面浏览器

##### 参数说明
无

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.hideFloatMenu({
  "ImageUrl": "xx",
  "floatTextList": "XX"
})
  .then((res) => {
    console.log(res);
  })
  .catch(error => {
    console.log(error);
  });
```

### 横竖屏切换

- **方法名称**: `setOrientation`
- **适用范围**: 页面浏览器

##### 返回值data说明
```json
{
  "code": 1,
  "message": "success"
}
```

##### 示例
```javascript
window.ado.setOrientation({
  "orientation": "landScape"
})
  .then((res) => {
  })
  .catch(error => {
    console.log(error);
  });
```

---

## 附录

### 小程序路由格式说明

小程序路由格式：
```
/mini/{appId}?path=urlencode(pages/index/index)&openType=refresh
```

- `appId`：小程序id
- `pages/index/index`：小程序页面路由
- `openType`: refresh会刷新小程序，否则只唤起已保活的小程序