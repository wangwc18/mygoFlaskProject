
function DecToRgbaColor(number) {

    const blue = number & 0xff;
    const green = number >> 8 & 0xff;
    const red = number >> 16 & 0xff;
    number = number >> 24 & 0xff;
    const alpha = (number / 0xff).toFixed(2);
    return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
}
function DecToRgbColor(number) {

    const blue = number & 0xff;
    const green = number >> 8 & 0xff;
    const red = number >> 16 & 0xff;
    number = number >> 24 & 0xff;
    return `rgb(${red}, ${green}, ${blue})`;
}


var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据:如果为ture表示正在加载数据；反之，没有加载数据



$(function () {
/**当主页加载完成之后，立即刷新主页的分页数据
* 默认加载第一页*/
    updateCommentPage();
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
            updateCommentPage()
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
        if ((canScrollHeight - nowScroll) < 150) {
            // 判断页数，去更新数据
            if (!data_querying) {
                // 表示正在加载数据
                data_querying = true;
                // 计算当前在第几页
                cur_page += 1;
                if (cur_page <= total_page) {
                    // 加载指定页码的数据
                    updateCommentPage();
                }
            }
        }
    })
});


function updateCommentPage() {
/** 更新一页（10条评论和回复）评论数据 */
    var params = {
        'cid':currentCid,
        'page':cur_page,
        'vid':vid
    };
    $.get('/api/comment', params, function (response) {
        // 得到响应后，表示一次加载数据结束了
        data_querying = false;
        if (response.errno == '0') {
            // 记录总页数
            total_page = response.totalPage;
            all_count = response.all_count
            $("#num_of_comment").html(all_count)
            var content =''
            if (cur_page == 1) {
                $("#comment-list").html("")
            }
            var top_num=0 //记录前n条是置顶评论
            if(response.top_replies!='' && response.top_replies!=null){ //包含置顶
                var replies = response.top_replies.concat(response.replies) //合并评论
                top_num = response.top_replies.length //记录置顶评论个数
            }else{
                var replies = response.replies
            }


            for (var i=0;i<replies.length;i++) {

content+='<div class="container p-0 pt-2 position-relative">'
                var reply = replies[i]
                if(reply.user_sailing!=null&&reply.user_sailing.image!=null&&reply.user_sailing.fan.color!=null){
                //有用户徽章
content+='<div class="reply-decorate">'
content+='<img src="'+reply.user_sailing.image+'" class="user-sailing-img"/>'
content+='<div class="user-sailing-text">'
content+='<span style="color:'+reply.user_sailing.fan.color+'">No:</span><br>'
content+='<span style="color:'+reply.user_sailing.fan.color+'">'+String(reply.user_sailing.fan.number).padStart(6, '0')+'</span>'
content+='</div>'
content+='</div>'
                }
content+='<div class="p-0 float-start root-reply-avatar">'
content+='<div class="d-flex justify-content-center">'
content+='<img class="bili-avatar-img" src="'+reply.avatar+'">'
content+='</div>'
                if(reply.pendant!='') { //有用户头像框
content += '<div class="position-relative">'
content += '<img class="bili-avatar-pendent-dom" src="'+reply.pendant+'"/>'
content += '</div>'
                }
content+='</div>'
content+='<div class="comment-right">'
content+='<div class="d-flex justify-content-start align-items-center ">'
                //用户是大会员，名字是粉色
                if(reply.vipStatus==1){
content+='<span class="ps-0 pe-2 comment-s-item-name2">'+reply.uname+'</span>'
                }else{
content+='<span class="ps-0 pe-2 comment-s-item-name">'+reply.uname+'</span>'
                }
                if(reply.current_level>=1&& reply.is_senior_member!=1){ //用户等级1-6
content+='<span class="ps-0 pe-2 level-img-wrap"><img src="/static/svg/l'+reply.current_level+'.svg" class="align-items-center level-img"></span>'
                }else if(reply.is_senior_member==1){ //用户是lv6硬核会员
content+='<span class="ps-0 pe-2 level-img-wrap"><img src="/static/svg/l6s.svg" class="align-items-center level-img"></span>'
                }else{ //用户没有等级显示lv0
content+='<span class="ps-0 pe-2 level-img-wrap"><img src="/static/svg/l0.svg" class="align-items-center level-img"></span>'
                }
                //用户是mygo粉丝
                if(reply.fans_detail!=null&&reply.fans_detail.medal_name!=null&&reply.fans_detail.level!=null) {
content += '<div class="fan-badge" style="background:'+DecToRgbaColor(reply.fans_detail.medal_color)+'">'
content += '<div class="badge-name-warp">'
content += '<div class="badge-name" style="color:'+DecToRgbaColor(reply.fans_detail.medal_color_name)+'">' + reply.fans_detail.medal_name + '</div>'
content += '</div>'
content += '<div class="badge-level-wrap" style="background:'+DecToRgbColor(reply.fans_detail.medal_level_bg_color)+'">'
content += '<div class="badge-level" style="color:'+DecToRgbaColor(reply.fans_detail.medal_color_level)+'">' + reply.fans_detail.level +'</div>'
content += '</div>'
content += '</div>'
                }
content += '</div>'
content+='<span class="p-0 reply-content">'
                if(top_num>i){ //置顶评论的"置顶"span
content+='<i class="reply-top-icon">置顶</i>'
                }
content+=reply.message
content+='</span>'
                if(reply.pictures!=null&&reply.pictures!=''&&reply.pictures.length>0){ //评论有图
content+='<div class="d-flex pt-2 flex-wrap">'
                    for(let k = 0; k　< reply.pictures.length; k++) {
                        //思路就是：图片的长和宽，短的那一条135px
                        if(reply.pictures[k].img_width>reply.pictures[k].img_height){
                            var style_str="width:"+Math.round(135*reply.pictures[k].img_width/reply.pictures[k].img_height)+";height:135px;"
                        }else{
                            var style_str="width:135px;height:"+Math.round(135*reply.pictures[k].img_height/reply.pictures[k].img_width)+"px;"
                        }
content+='<img class="p-1 rounded" src="'+reply.pictures[k].img_src+'" style="'+style_str+'"/>'
                        }
content+='</div>'
                }

content+='<div class="d-flex justify-content-start align-items-center py-2 reply-info ">'
content+='<span class="ps-0 pe-3">'+reply.ctime+'</span>'
content+='<span class="ps-0 pe-3"><img src="/static/svg/user-like-icon.svg" class="reply-op-icon"/>'
                if(reply.like!=0){ //点赞数为零不显示数字
content+= reply.like
                }
content+='</span>'
content+='<span class="ps-0 pe-3"><img src="/static/svg/user-dislike-icon.svg" class="reply-op-icon"/></span>'
content+='<span class="ps-0 pe-3">回复</span>'
content+='</div>'

                //下面的就是评论回复了
content+='<div class="p-0" id="r_'+reply.rpid+'">'
                for(let j = 0; j　< reply.replies.length; j++) {
                    var reply_reply = replies[i]
content+='<div class="container p-0 pt-1">'
content+='<div class="p-0 pt-2 float-start root-reply-avatar2">'
content+='<div class="d-flex justify-content-center">'
content+='<img class="bili-avatar-img2" src="'+reply.replies[j].avatar+'">'
content+='</div>'
content+='</div>'
content+='<div class="reply-right">'
content+='<div class="p-0 reply-content align-items-end">'
                    if(reply.replies[j].vipStatus==1){
content+='<span class="ps-0 pe-1 comment-s-item-name2">'+reply.replies[j].uname+'</span>'
                    }else{
content+='<span class="ps-0 pe-1 comment-s-item-name">'+reply.replies[j].uname+'</span>'
                    }
                    if(reply.current_level>=1&& reply.is_senior_member!=1){
content+='<span class="ps-0 pe-2" ><img src="/static/svg/l'+reply.current_level+'.svg" class="level-img"></span>'
                    } else if(reply.is_senior_member==1){
content+='<span class="ps-0 pe-2" ><img src="/static/svg/l6s.svg" class="level-img"></span>'
                    }else{
content+='<span class="ps-0 pe-2" ><img src="/static/svg/l0.svg" class="level-img"></span>'
                    }
content+= reply.replies[j].message
content+='</div>'
content+='<div class="d-flex justify-content-start align-items-center py-2 reply-info ">'
content+='<span class="ps-0 pe-3">'+reply.replies[j].ctime+'</span>'
content+='<span class="ps-0 pe-3"><img src="/static/svg/user-like-icon.svg" class="reply-op-icon"/>'
                    if(reply.replies[j].like!=0){
content+= reply.replies[j].like
                    }
content+= '</span>'
content+='<span class="ps-0 pe-3"><img src="/static/svg/user-dislike-icon.svg" class="reply-op-icon"/></span>'
content+='<span class="ps-0 pe-3">回复</span>'
content+='</div>'
content+='</div>'
content+='</div>'
                }
                if(reply.replies.length<reply.rcount) {
content+='<div class="d-flex">'
content+='<div class="p2 comment-view-more1">'+reply.sub_reply_entry_text+',</div>'
content+='<div class="p2 comment-view-more2" onClick="updateCommentMore('+reply.rpid+',1)">点击查看</div>'
content+='</div>'
                }
content+='<hr class="text-secondary">'
content+='</div>'
content+='</div>'
content+='</div>'
            }
            $("#comment-list").append(content);
        } else {
            alert(response.errmsg);
        }
    });
}





function updateCommentMore(rpid, page) {
/**
 *更新一页（一条评论的10条回复）回复数据
 */
    if(rpid==''|| rpid==null){
        return
    }
    if(page==''|| page==null){
        page = 0
    }
    var params = {
        'vid':vid,
        'rpid':rpid,
        'page':page,
        // 每页多少条不用传，默认10条
    };
     $.get('/api/comment_more', params, function (response) {
         if (response.errno == '0') {
             $("#r_"+rpid).html("")
             var replies = response.replies
             var content =''
content+='<div class="p-0" id="r_'+rpid+'">'
             for (var i=0;i<replies.length;i++) {
                var reply = replies[i]
content+='<div class="container p-0 pt-1">'
content+='<div class="p-0 pt-2 float-start root-reply-avatar2">'
content+='<div class="d-flex justify-content-center">'
content+='<img class="bili-avatar-img2" src="'+reply.avatar+'">'
content+='</div>'
content+='</div>'
content+='<div class="reply-right">'
content+='<div class="p-0 reply-content align-items-end">'

                        if(reply.vipStatus==1){
content+='<span class="ps-0 pe-1 comment-s-item-name2">'+reply.uname+'</span>'
                        }else{
content+='<span class="ps-0 pe-1 comment-s-item-name">'+reply.uname+'</span>'
                        }
                        if(reply.current_level>=1&& reply.is_senior_member!=1){
content+='<span class="ps-0 pe-2" ><img src="/static/svg/l'+reply.current_level+'.svg" class="level-img"></span>'
                        } else if(reply.is_senior_member==1){
content+='<span class="ps-0 pe-2" ><img src="/static/svg/l6s.svg" class="level-img"></span>'
                        }else{
content+='<span class="ps-0 pe-2" ><img src="/static/svg/l0.svg" class="level-img"></span>'
                        }

content+= reply.message
content+='</div>'
content+='<div class="d-flex justify-content-start align-items-center py-2 reply-info ">'
content+='<span class="ps-0 pe-3">'+reply.ctime+'</span>'
content+='<span class="ps-0 pe-3"><img src="/static/svg/user-like-icon.svg" class="reply-op-icon">'
                        if(reply.like!=0){
content+= reply.like
                        }
content+='</span>'
content+='<span class="ps-0 pe-3"><img src="/static/svg/user-dislike-icon.svg" class="reply-op-icon"></span>'
content+='<span class="ps-0 pe-3">回复</span>'
content+='</div>'
content+='</div>'
content+='</div>'
                    }
content+='<div class="d-flex justify-content-start">'
content+='<div class="px-2 comment-view-more-page-m">共'+Math.ceil(response.totalPage/10)+'页</div>'
                    for (var j=1;j<=Math.ceil(response.totalPage/10);j++) {
                        if(j==page){
content+='<div class="px-1 comment-view-more-page-active">'+j+'</div>'
                        }else{
content+='<div class="px-1 comment-view-more-page" onclick="updateCommentMore('+rpid+','+j+')">'+j+'</div>'
                        }
                    }
content+='</div>'
content+='<hr class="text-secondary">'
content+='</div>'
$("#r_"+rpid).html(content)
         }
     });
}


