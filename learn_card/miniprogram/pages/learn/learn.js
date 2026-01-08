// pages/learn/learn.js
const innerAudioContext = wx.createInnerAudioContext();

Page({
  data: {
    clickAreas: [],
    currentImage: ""
  },

  onLoad: function (options) {
    console.log("🔥 识字页启动，参数：", options);

    // 1. 设置图片 (从上一页传过来的远程图片地址)
    if (options.src) {
      this.setData({ currentImage: options.src });
    }

    // 2. 根据 key 去服务器拉取坐标配置
    if (options.key) {
      this.fetchConfig(options.key);
    }
  },

  // 新增：从服务器获取配置文件
  fetchConfig: function(sceneKey) {
    // 检查是否有缓存（可选优化），这里MVP直接每次请求
    wx.request({
      // 指向服务器上的那个 JSON 文件
      url: 'http://175.178.2.155/api/config/' + sceneKey, 
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200 && res.data) {
          // 1. 打印看看服务器到底给了什么（肯定是直接的数组）
          console.log(`✅ 服务器返回数据:`, res.data);

          const resultData = res.data;

          // 2. 直接使用数据，不要再用 [sceneKey] 去取了
          // 只要数据是个数组，且长度大于0，就说明是对的
          if (Array.isArray(resultData) && resultData.length > 0) {
             console.log(`✅ 成功加载场景 [${sceneKey}] 坐标`);
             
             this.setData({
               clickAreas: resultData
             });
          } else {
             // 如果返回的是空数组，或者格式不对
             console.warn(`⚠️ 场景 [${sceneKey}] 数据为空或格式异常`);
             this.setData({ clickAreas: [] });
          }
        }
      },
      fail: (err) => {
        console.error("❌ 配置文件下载失败", err);
        wx.showToast({ title: '数据加载失败', icon: 'none' });
      }
    });
  },

  onAreaClick: function (e) {
    if (!e || !e.currentTarget) return;
    const index = e.currentTarget.dataset.index;
    const item = this.data.clickAreas[index];
    
    if (item && item.audio) {
      console.log('🎵 播放:', item.text, item.audio);
      innerAudioContext.stop();
      innerAudioContext.src = item.audio; // 这里的 audio 已经是服务器上的 http 地址了
      innerAudioContext.play();
    }
  }
});