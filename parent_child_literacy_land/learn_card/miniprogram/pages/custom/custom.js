Page({
  data: {
    myCards: []
  },

  onShow() { this.fetchMyCards(); },

  fetchMyCards() {
    const uid = wx.getStorageSync('user_uid');
    if (!uid) return;
    wx.request({
      url: `http://175.178.2.155:8000/api/scenes?uid=${uid}`,
      success: (res) => {
        if (res.data) {
          const myScene = res.data.find(item => item.user_id == uid);
          if (myScene && myScene.images) {
            this.setData({ myCards: myScene.images });
          } else {
            this.setData({ myCards: [] });
          }
        }
      }
    });
  },

  // 1. 修改名称
  editName(e) {
    const { id, name } = e.currentTarget.dataset;
    wx.showModal({
      title: '修改名称',
      content: name,
      editable: true, // 开启输入框
      placeholderText: '请输入新名称',
      success: (res) => {
        if (res.confirm && res.content) {
          // 调用后端接口
          wx.request({
            url: 'http://175.178.2.155:8000/api/card/update_name',
            method: 'POST',
            data: { id: id, name: res.content },
            success: () => {
              wx.showToast({ title: '修改成功' });
              this.fetchMyCards(); // 刷新列表
            }
          });
        }
      }
    });
  },

  // 2. 删除
  deleteCard(e) {
    const id = e.currentTarget.dataset.id;
    wx.showModal({
      title: '警告',
      content: '确定要永久删除这张卡片吗？',
      confirmColor: '#FF0000',
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: 'http://175.178.2.155:8000/api/card/delete',
            method: 'POST',
            data: { id: id },
            success: () => {
              this.fetchMyCards();
            }
          });
        }
      }
    });
  },

// 跳转去编辑
toEdit(e) {
  const item = e.currentTarget.dataset.item;
  // 传递 key 和 url，标记 mode=edit
  wx.navigateTo({
    url: `/pages/create/create?mode=edit&key=${item.card_key}&img=${encodeURIComponent(item.image_url)}`
  });
},

  toDetail(e) {
    const idx = e.currentTarget.dataset.idx;
    const img = this.data.myCards[idx];
    wx.navigateTo({ url: `/pages/learn/learn?key=${img.key}&src=${img.src}` });
  },
  
  toCreate() { wx.navigateTo({ url: '/pages/create/create' }); }
});