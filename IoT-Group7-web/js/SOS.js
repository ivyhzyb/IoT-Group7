// 获取按钮元素
const callButton = document.getElementById("callButton");

// 添加点击事件处理程序
callButton.addEventListener("click", function () {
  // 触发电话拨打功能
  window.location.href = "tel:000";
});
