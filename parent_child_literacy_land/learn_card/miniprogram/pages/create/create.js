Page({
  data: {
    tempImagePath: '', // 本地显示用的图片路径
    serverImageUrl: '', // 上传成功后的服务器URL
    hotspots: [], // 热区数据
    imgInfo: { width: 0, height: 0 }, // 图片实际渲染尺寸
    
    // 编辑弹窗相关
    isEditing: false,
    editIndex: -1,
    currentText: '',

    // 模式控制
    isEditMode: false, // 是否为编辑模式
    cardKey: ''        // 编辑模式下的卡片Key
  },

  // --- 1. 页面加载：判断模式 ---
  onLoad: function (options) {
    // 如果带有 mode=edit 参数，说明是二次编辑
    if (options.mode === 'edit') {
      const imgUrl = decodeURIComponent(options.img);
      const cardKey = options.key;
      
      this.setData({
        serverImageUrl: imgUrl,
        tempImagePath: imgUrl, // 直接显示网络图片
        isEditMode: true,
        cardKey: cardKey
      });
      
      // 去服务器拉取已有的热区数据
      this.fetchHotspots(cardKey);
    }
  },

  // 拉取现有热区数据
  fetchHotspots(cardKey) {
    wx.showLoading({ title: '加载数据...' });
    wx.request({
      url: `http://175.178.2.155:8000/api/config/${cardKey}`,
      success: (res) => {
        if (res.data && Array.isArray(res.data)) {
          this.setData({ hotspots: res.data });
        }
      },
      complete: () => wx.hideLoading()
    });
  },

  // --- 2. 图片选择与上传 (新建模式用) ---
  chooseImage() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      success: (res) => {
        const tempPath = res.tempFiles[0].tempFilePath;
        this.setData({ tempImagePath: tempPath });
        // 选完图立即上传并分析
        this.uploadAndAnalyze(tempPath);
      }
    });
  },

  // 图片加载完成，获取实际宽高 (用于计算拖拽坐标)
  onImgLoad(e) {
    const query = wx.createSelectorQuery();
    query.select('.bg-img').boundingClientRect(rect => {
      this.setData({ imgInfo: { width: rect.width, height: rect.height } });
    }).exec();
  },

  // 上传 + AI分析
  uploadAndAnalyze(filePath) {
    wx.showLoading({ title: 'AI分析中...', mask: true });
    
    // A. 上传
    wx.uploadFile({
      url: 'http://175.178.2.155:8000/api/upload', 
      filePath: filePath,
      name: 'file',
      success: (res) => {
        try {
          const data = JSON.parse(res.data);
          if (data.code === 200) {
            const serverUrl = data.url;
            this.setData({ serverImageUrl: serverUrl });
            
            // B. 分析
            wx.request({
              url: 'http://175.178.2.155:8000/api/analyze',
              method: 'POST',
              data: { image_url: serverUrl },
              success: (aiRes) => {
                if (aiRes.data.code === 200 && aiRes.data.data) {
                  this.setData({ hotspots: aiRes.data.data });
                  wx.showToast({ title: '识别完成', icon: 'success' });
                } else {
                  wx.showToast({ title: '未识别到物体', icon: 'none' });
                }
              },
              complete: () => wx.hideLoading()
            });
          } else {
            wx.hideLoading();
            wx.showToast({ title: '上传服务端错误', icon: 'none' });
          }
        } catch (e) {
          wx.hideLoading();
          console.error(e);
        }
      },
      fail: (err) => { 
        wx.hideLoading(); 
        console.error(err);
        wx.showToast({ title: '上传请求失败', icon: 'none' }); 
      }
    });
  },

  // --- 3. 交互逻辑 ---

  // 拖拽移动
  onBoxMove(e) {
    if (e.detail.source === 'touch') {
      const idx = e.currentTarget.dataset.index;
      const { x, y } = e.detail;
      const { width, height } = this.data.imgInfo;
      // 反算百分比
      const list = this.data.hotspots;
      list[idx].rect[0] = x / width;
      list[idx].rect[1] = y / height;
      // 内存更新，不频繁setData防止卡顿
      this.data.hotspots = list;
    }
  },

  // 缩放 (占位，MVP暂不处理复杂缩放)
  onBoxScale(e) {},

  // 编辑文字
  editTag(e) {
    const idx = e.currentTarget.dataset.index;
    this.setData({
      isEditing: true,
      editIndex: idx,
      currentText: this.data.hotspots[idx].text
    });
  },

  onInputText(e) {
    this.setData({ currentText: e.detail.value });
  },

  // 确认修改/添加
  confirmText() {
    const { editIndex, currentText, hotspots } = this.data;
    if (!currentText) return;

    if (editIndex >= 0) {
      // 修改现有
      hotspots[editIndex].text = currentText;
      hotspots[editIndex].pinyin = ''; // 修改文字后拼音清空，等后端重新生成或忽略
      this.setData({ hotspots, isEditing: false });
    } else {
      // 新增
      const newBox = {
        text: currentText,
        pinyin: '', 
        rect: [0.4, 0.4, 0.2, 0.1] // 默认位置
      };
      this.setData({ hotspots: [...hotspots, newBox], isEditing: false });
    }
  },
  
  cancelText() {
    this.setData({ isEditing: false, editIndex: -1 });
  },

  // 手动添加按钮
  startAddBox() {
    this.setData({ isEditing: true, editIndex: -1, currentText: '' });
  },

  // 删除按钮
  deleteBox(e) {
    const idx = e.currentTarget.dataset.index;
    const list = this.data.hotspots;
    list.splice(idx, 1);
    this.setData({ hotspots: list });
  },

  // --- 4. 提交保存 (核心分支逻辑) ---
  submitToServer() {
    const uid = wx.getStorageSync('user_uid');
    if (!uid) return wx.showToast({ title: '请先登录', icon: 'none' });
    if (!this.data.serverImageUrl) return wx.showToast({ title: '图片未上传', icon: 'none' });

    wx.showLoading({ title: '保存中...' });

    if (this.data.isEditMode) {
      // 🟢 分支 A：编辑模式 -> 调用更新接口 (只更新热区)
      wx.request({
        url: 'http://175.178.2.155:8000/api/admin/save_hotspots',
        method: 'POST',
        data: {
          card_key: this.data.cardKey,
          hotspots: this.data.hotspots
        },
        success: (res) => {
          wx.hideLoading();
          if (res.data.code === 200) {
            wx.showToast({ title: '更新成功' });
            setTimeout(() => wx.navigateBack(), 1500);
          } else {
            wx.showModal({ title: '更新失败', content: res.data.msg, showCancel: false });
          }
        },
        fail: () => {
          wx.hideLoading();
          wx.showToast({ title: '网络错误', icon: 'none' });
        }
      });

    } else {
      // 🔵 分支 B：新建模式 -> 调用创建接口
      wx.request({
        url: 'http://175.178.2.155:8000/api/user/create_card',
        method: 'POST',
        data: {
          uid: uid,
          scene_title: "我的上传",
          image_url: this.data.serverImageUrl,
          hotspots: this.data.hotspots
        },
        success: (res) => {
          wx.hideLoading();
          if (res.data.code === 200) {
            wx.showToast({ title: '保存成功' });
            setTimeout(() => wx.navigateBack(), 1500);
          } else {
            wx.showModal({ title: '保存失败', content: res.data.msg, showCancel: false });
          }
        },
        fail: () => {
          wx.hideLoading();
          wx.showToast({ title: '网络错误', icon: 'none' });
        }
      });
    }
  }
});