var kyoPopupMenu={};
var file_name ="" ;
var con_name = "";

//获取GET值
function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}



//获取点击事件的值
function myname(event) {
    var btnNum = event.button;
    if(btnNum==2){
        file_name = event.target.innerHTML.replace(/(^\s*)|(\s*$)/g, "")
        console.log(file_name)
    }
    con_name = GetQueryString("dir")
    console.log(GetQueryString("dir"))
}


    kyoPopupMenu = (function(){
        return {
            sys: function (obj) {
                $('.popup_menu').remove();
                popupMenuApp = $('<div class="popup_menu app-menu"><ul><li><a menu="menu1">下载</a></li><li><a menu="menu2">删除</a></li></ul></div>')
                .find('a').attr('href','javascript:;')
                .end().appendTo('body');
                //绑定事件
                $('.app-menu a[menu="menu1"]').on('click', function (){
                    console.log("ok");
                    console.log($(this).find("p").value);
                    window.location.href="/lpan/download/?filename="+file_name+"&con_name="+con_name;
                });
                $('.app-menu a[menu="menu2"]').on('click', function (){
                    window.location.href="/lpan/delete/?file_name="+file_name+"&con_name="+con_name;
                });
                return popupMenuApp;
            }
    }})();
    //取消右键
    $('html').on('contextmenu', function (){return false;}).click(function(){
        $('.popup_menu').hide();
    });
    //模块点击右击
    $('.detail').on('contextmenu',function (e){
        var popupmenu = kyoPopupMenu.sys();
        l = ($(document).width() - e.clientX) < popupmenu.width() ? (e.clientX - popupmenu.width()) : e.clientX;
        t = ($(document).height() - e.clientY) < popupmenu.height() ? (e.clientY - popupmenu.height()) : e.clientY;
                        popupmenu.css({left: l,top: t}).show();
        return false;
    });



  //  弹出框js
  $(document).on('opening', '.remodal', function () {
    console.log('opening');
  });

  $(document).on('opened', '.remodal', function () {
    console.log('opened');
  });

  $(document).on('closing', '.remodal', function (e) {
    console.log('closing' + (e.reason ? ', reason: ' + e.reason : ''));
  });

  $(document).on('closed', '.remodal', function (e) {
    console.log('closed' + (e.reason ? ', reason: ' + e.reason : ''));
  });

  $(document).on('confirmation', '.remodal', function () {
    console.log('confirmation');
  });

  $(document).on('cancellation', '.remodal', function () {
    console.log('cancellation');
  });

