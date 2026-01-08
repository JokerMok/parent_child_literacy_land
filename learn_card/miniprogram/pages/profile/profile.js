Page({
  data: {
    isLogin: false,
    uid: '',
    versionStr: '',
    userInfo: {
      nickName: '',
      avatarUrl: ''
    },
    // 新增：统计数据
    stats: {
      days: 0,
      words: 0,
      badges: 0
    },
    // 新增：VIP状态
    vipInfo: {
      isVip: false,
      expireTime: ''
    },
    // 新增：声音克隆状态
    voiceCloneInfo: {
      hasClonedVoice: false,
      voiceId: ''
    }
  },

  onShow() {
    // 每次显示页面，不仅检查本地，还要去服务器拉取最新数据
    this.checkLoginStatusAndFetch();
    this.fetchSystemVersion(); 
  },

  checkLoginStatusAndFetch() {
    const localUid = wx.getStorageSync('user_uid');
    
    if (localUid) {
      // 1. 先显示本地缓存（为了快）
      const localInfo = wx.getStorageSync('user_info');
      if (localInfo) {
        this.setData({ isLogin: true, uid: localUid, userInfo: localInfo });
      }

      // 2. 这里的关键：去服务器拿最新的（包括统计数据）
      wx.request({
        url: 'http://175.178.2.155:8000/api/user/' + localUid,
        method: 'GET',
        success: (res) => {
          if (res.data.uid) {
            console.log("✅ 从数据库同步最新数据:", res.data);
            
            const serverData = res.data;
            // 更新页面数据
            this.setData({
              isLogin: true,
              uid: serverData.uid,
              userInfo: {
                nickName: serverData.nickName,
                avatarUrl: serverData.avatarUrl
              },
              stats: serverData.stats, // 更新统计数据
              vipInfo: {
                isVip: serverData.is_vip === 1,
                expireTime: serverData.vip_expire_time
              },
              voiceCloneInfo: {
                hasClonedVoice: !!serverData.voice_id,
                voiceId: serverData.voice_id
              }
            });
            
            // 更新本地缓存
            wx.setStorageSync('user_info', {
                nickName: serverData.nickName,
                avatarUrl: serverData.avatarUrl
            });
          }
        }
      });
    } else {
      this.setData({ isLogin: false });
    }
  },

  handleLogin() {
    // ... 保持之前的登录逻辑不变 ...
    // 为了节省篇幅，这里省略 getUserProfile -> login 的代码
    // 请保留你之前写好的 handleLogin 代码
    if (this.data.isLogin) return;
    wx.getUserProfile({
        desc: '用于完善会员资料',
        success: (resProfile) => {
            const userInfo = resProfile.userInfo;
            wx.showLoading({ title: '登录中...' });
            wx.login({
                success: (resLogin) => {
                    if (resLogin.code) {
                        wx.request({
                            url: 'http://175.178.2.155:8000/api/login',
                            method: 'POST',
                            data: { code: resLogin.code, userInfo: userInfo },
                            success: (apiRes) => {
                                if (apiRes.data.uid) {
                                    const userData = apiRes.data;
                                    // 保存 UID
                                    wx.setStorageSync('user_uid', userData.uid);
                                    // 登录成功后，立刻刷新一次全量数据
                                    this.checkLoginStatusAndFetch();
                                    wx.showToast({ title: '登录成功' });
                                }
                            },
                            complete: () => wx.hideLoading()
                        });
                    }
                }
            });
        }
    });
  },

  onChooseAvatar(e) {
    const { avatarUrl } = e.detail;
    // 更新本地
    const newUserInfo = { ...this.data.userInfo, avatarUrl: avatarUrl };
    this.setData({ userInfo: newUserInfo });
    
    // 同步给数据库
    this.updateUserProfileToBackend(this.data.userInfo.nickName, avatarUrl);
  },

  onNicknameChange(e) {
    const nickName = e.detail.value;
    // 更新本地
    const newUserInfo = { ...this.data.userInfo, nickName: nickName };
    this.setData({ userInfo: newUserInfo });

    // 同步给数据库
    this.updateUserProfileToBackend(nickName, this.data.userInfo.avatarUrl);
  },

  // 【核心修改】调用真正的更新接口
  updateUserProfileToBackend(nickName, avatarUrl) {
    const uid = this.data.uid;
    if (!uid) return;

    wx.request({
      url: 'http://175.178.2.155:8000/api/user/update',
      method: 'POST',
      data: {
        uid: uid,
        nickname: nickName,
        avatar_url: avatarUrl // 注意这里字段名要和 Python 定义的一致
      },
      success: (res) => {
        console.log("✅ 个人资料已同步至数据库");
      }
    });
  },

  toMyCustom() {
    wx.navigateTo({ url: '/pages/custom/custom' });
  },

  // 跳转到声音克隆页面
  toVoiceStudio() {
    wx.navigateTo({ url: '/pages/voice-studio/voice-studio' });
  },

  // 跳转到VIP页面
  toVipCenter() {
    wx.navigateTo({ url: '/pages/vip-center/vip-center' });
  },
  
  // 增加获取配置的方法
  showVersion() {
    this.fetchConfigAndShow('version_info', '版本内容');
  },

  showAgreement() {
    this.fetchConfigAndShow('user_agreement', '用户协议');
  },

  fetchConfigAndShow(key, title) {
    wx.showLoading();
    wx.request({
      url: 'http://175.178.2.155:8000/api/system/config',
      success: (res) => {
        const content = res.data[key] || '暂无内容';
        wx.showModal({
          title: title,
          content: content,
          showCancel: false,
          confirmText: '知道了'
        });
      },
      complete: () => wx.hideLoading()
    });
  },
  
  // 可以在 onShow 里检查权限，如果 enable_upload 是 false，就隐藏上传入口
  // 这部分逻辑你可以根据需要加在 custom.js 或 home.js 里

  fetchSystemVersion() {
    wx.request({
      url: 'http://175.178.2.155:8000/api/system/config',
      success: (res) => {
        if (res.data && res.data.version_number) {
          this.setData({
            versionStr: res.data.version_number
          });
        }
      }
    });
  },

  handleLogout() {
    wx.showModal({
      title: '提示', content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          this.setData({ isLogin: false, uid: '', userInfo: {}, stats: { days:0, words:0, badges:0 } });
        }
      }
    })
  }
});