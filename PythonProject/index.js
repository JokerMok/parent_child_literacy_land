// 创建内部 audio 上下文
const innerAudioContext = wx.createInnerAudioContext();

Page({
  data: {
    clickAreas: []  // 点击区域数据
  },

  onLoad: function () {
    this.loadConfig();
  },

  // 加载配置文件
  loadConfig: function () {
    const that = this;
    
    // 读取本地 config.json 文件
    wx.request({
      url: 'config.json',  // 如果是本地文件，可能需要放在合适位置
      method: 'GET',
      success: function (res) {
        that.setData({
          clickAreas: res.data
        });
      },
      fail: function (error) {
        console.error('加载配置文件失败:', error);
        
        // 如果直接请求失败，尝试使用 require 方式
        try {
          const config = require('../../config.json'); // 根据实际路径调整
          that.setData({
            clickAreas: config
          });
        } catch (e) {
          console.error('读取配置文件失败:', e);
        }
      }
    });
  },

  // 区域点击事件
  onAreaClick: function (event) {
    const index = event.currentTarget.dataset.index;
    const area = this.data.clickAreas[index];
    
    console.log('点击了区域:', area.text);
    
    // 播放对应音频
    this.playAudio(area.audio);
  },

  // 播放音频
  playAudio: function (audioPath) {
    // 停止当前音频
    innerAudioContext.stop();
    
    // 设置音频源
    innerAudioContext.src = audioPath;
    
    // 播放音频
    innerAudioContext.play();
    
    // 监听播放错误
    innerAudioContext.onError((res) => {
      console.error('音频播放失败:', res.errMsg);
    });
    
    // 监听播放结束
    innerAudioContext.onEnded(() => {
      console.log('音频播放结束');
    });
  }
});
