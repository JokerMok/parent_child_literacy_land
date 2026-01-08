Page({
  startRandom: function() {
    wx.showLoading({ title: '准备中...' });

    // 1. 先去服务器拿数据
    wx.request({
      url: 'http://175.178.2.155/api/scenes',
      success: (res) => {
        if (res.statusCode === 200 && res.data) {
          const sceneList = res.data;
          
          // 2. 拍扁数组，取出所有图片
          let allImages = [];
          sceneList.forEach(scene => {
            allImages = allImages.concat(scene.images);
          });

          // 3. 随机抽一个
          if (allImages.length > 0) {
            const randomIndex = Math.floor(Math.random() * allImages.length);
            const targetImage = allImages[randomIndex];

            // 4. 跳转
            wx.navigateTo({
              url: `/pages/learn/learn?key=${targetImage.key}&src=${targetImage.src}`
            });
          }
        }
      },
      fail: () => {
        wx.showToast({ title: '无法连接服务器', icon: 'none' });
      },
      complete: () => {
        wx.hideLoading();
      }
    });
  }
});