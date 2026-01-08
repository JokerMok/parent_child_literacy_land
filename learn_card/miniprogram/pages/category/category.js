// pages/category/category.js
Page({
  data: {
    scenes: []
  },

  onShow: function() {
    this.fetchData();
  },

  fetchData: function() {
    const uid = wx.getStorageSync('user_uid') || 0;
    wx.showLoading({ title: '加载中...' });
    
    wx.request({
      // 注意：这里是反引号 ` 
      url: `http://175.178.2.155:8000/api/scenes?uid=${uid}`,
      method: 'GET',
      success: (res) => {
        console.log("✅ 场景列表加载成功:", res.data);
        if (res.statusCode === 200 && res.data) {
          this.setData({
            scenes: res.data
          });
        }
      },
      fail: (err) => {
        console.error("❌ 加载失败:", err);
        wx.showToast({ title: '网络开小差了', icon: 'none' });
      },
      complete: () => {
        wx.hideLoading();
      }
    });
  },

  toDetail: function(e) {
    const idx = e.currentTarget.dataset.idx;
    const scene = this.data.scenes[idx];
    const currentUid = wx.getStorageSync('user_uid');

    // 1. 逻辑修正：如果是用户自己的场景，跳转到【我的作品集】页面去选图
    if (scene.user_id && scene.user_id == currentUid) {
      wx.navigateTo({
        url: '/pages/custom/custom'
      });
      return;
    }

    // 2. 官方场景：保持原有逻辑
    if (!scene.images || scene.images.length === 0) {
      wx.showToast({ title: '该场景暂无内容', icon: 'none' });
      return;
    }
    
    const firstImg = scene.images[0];
    
    // 跳转到识字页
    wx.navigateTo({
      url: `/pages/learn/learn?key=${firstImg.key}&src=${firstImg.src}`
    });
  }
});