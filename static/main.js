
var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据:如果为ture表示正在加载数据；反之，没有加载数据
$(function () {
    $.get('/api/danmu?id='+vid,function (response){
        const items = response.data
        const player = new NPlayer.Player({
           src: "/api/video?vid="+vid,
           plugins: [
            new NPlayerDanmaku({items}),
        ],
       });
       player.mount('#dplayer')
   })


    // 当主页加载完成之后，立即刷新主页的分页数据
    // 默认加载第一页
    updateNewsData();
    // 首页分类切换
    $('.hot_or_new').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.hot_or_new').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')
        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid;
            // 重置分页参数
            cur_page = 1;
            total_page = 1;
            updateNewsData()
        }
    });
    //页面滚动加载相关
    $(window).scroll(function () {
        // 浏览器窗口高度
        var showHeight = $(window).height();
        // 整个网页的高度
        var pageHeight = $(document).height();
        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;
        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();
        if ((canScrollHeight - nowScroll) < 20) {
            // TODO 判断页数，去更新新闻数据
            if (!data_querying) {
                // 表示正在加载数据
                data_querying = true;
                // 计算当前在第几页
                cur_page += 1;
                if (cur_page <= total_page) {
                    // 加载指定页码的新闻数据
                    updateNewsData();
                }
            }
        }
    })
});
function updateNewsData() {
    // TODO 更新新闻数据
    var params = {
        'cid':currentCid,
        'page':cur_page,
        'vid':vid
        // 每页多少条不用传，默认10条
    };
    $.get('/api/comment', params, function (response) {
        // 得到响应后，表示一次加载数据结束了
        data_querying = false;
        if (response.errno == '0') {
            // 记录总页数
            total_page = response.totalPage;
            var content =''
            if (cur_page == 1) {
                $(".comment-list").html("");
                if(response.top_replies!='' && response.top_replies!=null){
                for (var i=0;i<response.top_replies.length;i++) {
                    var reply = response.top_replies[i]
                    content += '<div class="comment--item">'
                    if(reply.user_sailing!=null&&reply.user_sailing.image!=null&&reply.user_sailing.fan.color!=null){
                        content += '<div class="user-right-top-band"><img src="'+reply.user_sailing.image+'" class="user-right-top-band-img"/>'
                        content +='<div class="user-right-top-band-num">'
                        content +='<span style="color:'+reply.user_sailing.fan.color+'">No:</span><br>'
                        content +='<span style="color:'+reply.user_sailing.fan.color+'">'+reply.user_sailing.fan.number+'</span>'
                        content +='</div>'
                        content +='</div>'
                    }
                    content += '<div class="comment-item-img-contain">'
                    content += '<div class="comment-item-img1">'
                    content += '<img class="comment-item-img-1" src="'+reply.avatar+'" />'
                    content += '</div>'
                    content += '<div class="comment-item-img2">'
                    if(reply.pendant!=''){
                        content += '<img class="comment-item-img-2" src="'+reply.pendant+'" />'}
                    content += '</div>'
                    content += '</div>'
                    content += '<div class="comment-item-right">'
                    content += '<div class="comment-item-name">'
                    if(reply.vipStatus==1){
                        content += '<span>'+reply.uname+'</span>'}
                    else{
                        content += '<span>'+reply.uname+'</span>'}
                    if(reply.current_level>=1&& reply.is_senior_member!=1)
                        content += '<span style="padding-left:5px"><img style="height:13px;width:26px" src="/static/pic/l'+reply.current_level+'.png"/></span></div>'
                    else if(reply.is_senior_member==1)
                        content += '<span style="padding-left:5px"><img style="height:13px;width:26px" src="/static/pic/l6s.png"/></span></div>'
                    else
                        content += '<span style="padding-left:5px"><img style="height:13px;width:26px" src="/static/pic/l0.png"/></span></div>'
                    content += '<div class="comment-item-content"><i class="go-top-icon">置顶</i>'+reply.message+'</div>'
                    if(reply.pictures!=null&&reply.pictures!=''&&reply.pictures.length>0){
                        for(let k = 0; k　< reply.pictures.length; k++){
                        content += '<div style="padding-left:10px"><img src="'+reply.pictures[k].img_src+'" style="width:'+Math.round(reply.pictures[k].img_width/3)+'px;height:'+Math.round(reply.pictures[k].img_height/3)+'px"/></div>'
                        }
                    }
                    content += '<div class="comment-item-fun">'+reply.ctime
                    content += '<span style="padding-left:25px"><img src="/static/svg/user-like-icon.svg" style="vertical-align: middle;height:18px"/></span>'
                    content += '<span style="padding-left:2px">'+reply.like+'</span>'
                    content += '<span style="padding-left:25px"><img src="/static/svg/user-dislike-icon.svg" style="vertical-align: middle;;height:18px"/></span>'
                    content += '<span style="padding-left:25px">回复</span>'
                    content += '</div>'
                    for(let j = 0; j　< reply.replies.length; j++) {
                        content += '<div class="comment-s-item">'
                        content += '<div class="comment-s-item-img-contain">'
                        content += '<div class="comment-s-item-img1">'
                        content += '<img class="comment-s-item-img-1" src="'+reply.replies[j].avatar+'" />'
                        content += '</div>'
                        content += '</div>'
                        content += '<div class="comment-s-item-right">'
                        if(reply.replies[j].vipStatus==1){
                            content += '<span class="comment-s-item-name2">'+reply.replies[j].uname+'</span>'
                        }
                        else{
                            content += '<span class="comment-s-item-name">'+reply.replies[j].uname+'</span>'}
                        if(reply.current_level>=1&& reply.is_senior_member!=1)
                            content += '<span style="padding-left:5px"><img style="height:12px;width:24px" src="/static/pic/l'+reply.current_level+'.png"/></span>'
                        else if(reply.is_senior_member==1)
                            content += '<span style="padding-left:5px"><img style="height:12px;width:24px" src="/static/pic/l6s.png"/></span>'
                        else
                            content += '<span style="padding-left:5px"><img style="height:12px;width:24px" src="/static/pic/l0.png"/></span>'
                        content += '<span class="comment-s-item-content">'+reply.replies[j].message+'</span>'
                        content += '<div class="comment-s-item-fun">'+reply.replies[j].ctime
                        content += '<span style="padding-left:25px"><img src="/static/svg/user-like-icon.svg" style="vertical-align: middle;height:18px"/></span>'
                        content += '<span style="padding-left:2px">'+reply.replies[j].like+'</span>'
                        content += '<span style="padding-left:25px"><img src="/static/svg/user-dislike-icon.svg" style="vertical-align: middle;;height:18px"/></span>'
                        content += '<span style="padding-left:25px">回复</span>'
                        content += '</div>'
                        content += '</div>'
                        content += '</div>'
                    }
                    if(reply.replies.length>0) {
                        content += '<div style="font-size:13px;color:#9499A0;padding-left:10px;padding-top:10px">'+reply.sub_reply_entry_text+',点击查看</div>'
                    }
                    content += '<div class = "bottom-line" > </div>'
                    content += '</div>'
                    content += '</div>'
                    //
                }
                }
            }
            for (var i=0;i<response.replies.length;i++) {
                var reply = response.replies[i]
content += '<div class="comment--item">'
                if(reply.user_sailing!=null&&reply.user_sailing.image!=null&&reply.user_sailing.fan.color!=null){
content += '<div class="user-right-top-band"><img src="'+reply.user_sailing.image+'" class="user-right-top-band-img"/>'
content +='<div class="user-right-top-band-num">'
content +='<span style="color:'+reply.user_sailing.fan.color+'">No:</span><br>'
content +='<span style="color:'+reply.user_sailing.fan.color+'">'+reply.user_sailing.fan.number+'</span>'
content +='</div>'
content +='</div>'
                }

content += '<div class="comment-item-img-contain">'
content += '<div class="comment-item-img1">'
content += '<img class="comment-item-img-1" src="'+reply.avatar+'" />'
content += '</div>'
content += '<div class="comment-item-img2">'
                if(reply.pendant!=''){
content += '<img class="comment-item-img-2" src="'+reply.pendant+'" />'}
content += '</div>'
content += '</div>'
content += '<div class="comment-item-right">'
content += '<div class="comment-item-name">'
                if(reply.vipStatus==1){
content += '<span style="color:#FB7299;">'+reply.uname+'</span>'}
                else{
content += '<span>'+reply.uname+'</span>'}
                if(reply.current_level>=1&& reply.is_senior_member!=1)
content += '<span style="padding-left:5px"><img style="height:13px;width:26px" src="/static/pic/l'+reply.current_level+'.png"/></span></div>'
                else if(reply.is_senior_member==1)
content += '<span style="padding-left:5px"><img style="height:13px;width:26px" src="/static/pic/l6s.png"/></span></div>'
                else
content += '<span style="padding-left:5px"><img style="height:13px;width:26px" src="/static/pic/l0.png"/></span></div>'

content += '<div class="comment-item-content">'+reply.message+'</div>'
                if(reply.pictures!=null&&reply.pictures!=''&&reply.pictures.length>0){
                    for(let k = 0; k　< reply.pictures.length; k++){
content += '<div style="padding-left:10px"><img src="'+reply.pictures[k].img_src+'" style="width:'+Math.round(reply.pictures[k].img_width/3)+'px;height:'+Math.round(reply.pictures[k].img_height/3)+'px"/></div>'
                    }
                }
content += '<div class="comment-item-fun">'+reply.ctime
content += '<span style="padding-left:25px"><img src="/static/svg/user-like-icon.svg" style="vertical-align: middle;height:18px"/></span>'
content += '<span style="padding-left:2px">'+reply.like+'</span>'
content += '<span style="padding-left:25px"><img src="/static/svg/user-dislike-icon.svg" style="vertical-align: middle;;height:18px"/></span>'
content += '<span style="padding-left:25px">回复</span>'
content += '</div>'

                for(let j = 0; j　< reply.replies.length; j++) {
content += '<div class="comment-s-item">'
content += '<div class="comment-s-item-img-contain">'
content += '<div class="comment-s-item-img1">'
content += '<img class="comment-s-item-img-1" src="'+reply.replies[j].avatar+'" />'
content += '</div>'
content += '</div>'
content += '<div class="comment-s-item-right">'
if(reply.replies[j].vipStatus==1){
    content += '<span class="comment-s-item-name2">'+reply.replies[j].uname+'</span>'
}
else{
    content += '<span class="comment-s-item-name">'+reply.replies[j].uname+'</span>'}
                if(reply.current_level>=1&& reply.is_senior_member!=1)
content += '<span style="padding-left:5px"><img style="height:12px;width:24px" src="/static/pic/l'+reply.current_level+'.png"/></span>'
                else if(reply.is_senior_member==1)
content += '<span style="padding-left:5px"><img style="height:12px;width:24px" src="/static/pic/l6s.png"/></span>'
                else
content += '<span style="padding-left:5px"><img style="height:12px;width:24px" src="/static/pic/l0.png"/></span>'

content += '<span class="comment-s-item-content">'+reply.replies[j].message+'</span>'
content += '<div class="comment-s-item-fun">'+reply.replies[j].ctime
content += '<span style="padding-left:25px"><img src="/static/svg/user-like-icon.svg" style="vertical-align: middle;height:18px"/></span>'
content += '<span style="padding-left:2px">'+reply.replies[j].like+'</span>'
content += '<span style="padding-left:25px"><img src="/static/svg/user-dislike-icon.svg" style="vertical-align: middle;;height:18px"/></span>'
content += '<span style="padding-left:25px">回复</span>'
content += '</div>'
content += '</div>'
content += '</div>'
}
if(reply.replies.length>0) {
content += '<div style="font-size:13px;color:#9499A0;padding-left:10px;padding-top:10px">'+reply.sub_reply_entry_text+',点击查看</div>'
}
content += '<div class = "bottom-line" > </div>'
content += '</div>'
content += '</div>'


            }
            $(".comment-list").append(content);
        } else {
            alert(response.errmsg);
        }
    });
}