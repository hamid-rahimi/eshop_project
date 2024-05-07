function sendArticleComment(articleId) {
    var message = document.getElementById('send-comment').value;
    var article_id = articleId;
    var parentId = $('#parent_id').val();
    console.log(parentId);

    $.get("/blog/submit-comment/", {
        comment: message,
        article_id: article_id,
        parent_id: parentId
    }).then(res => {
        $('#reload-comment').html(res); // نمایش پیام با��گشت
        var commentId = $('#set-comment-id').val();
        console.log(commentId);
        console.log('comment-location-' + commentId);
        if (parentId !== null && parentId !== "") {
            document.getElementById('comment-location-' + parentId).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('reload-comment').scrollIntoView({behavior: "smooth"});
        }

        document.getElementById('send-comment').value = ''; // پاک کردن فرم
        $('#parent_id').val(null);
        $('#set-comment-id').val(null);

        if (res.success) {
            document.getElementById('send-comment').value = ''; // پاک کردن فرم
            
        }

     });
}

function sendReplayComment(commentId) {
    $('#parent_id').val(commentId);
    console.log(commentId);
    document.getElementById('writeComment').scrollIntoView({behavior: "smooth"});
}

function filterPriceButton() {

    const priceValue = $('#sl2').val();
    var startPrice = priceValue.split(',')[0];
    var endPrice = priceValue.split(',')[1];
    $('#start_price').val(startPrice);
    $('#end_price').val(endPrice);
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}

function addToFavoriteProduct(productId, userId) {
    // debugger;
    var productId = productId;
    var userId = userId;
    $.get("/home-page/favorite-product/", {
        product_id: productId,
        user_id: userId
    }).then(res => {
        $('#reload_favorite').html(res);
    });
}

function showLargeProductImage(imageSrc) {
    console.log(imageSrc);
    $('#main_product_image').attr('src', imageSrc);
    $('#show_large_main_pic').attr('href', imageSrc);
}

function delete_from_favorite_list(product_id, user_id) {
    var productId = product_id;
    var userId = user_id;
    $.get("/home-page/favorite-product/", {
        product_id: productId,
        user_id: userId,
        method: 'delete'
    }).then(res => {
        window.location.reload();
        console.log(res);
        // $('#reload_favorite').html(res);
    });
}

function addToProductOrderList(productId) {
    // debugger
    var count = +document.getElementsByName('count_of_product')[0].value || 1;
    if (!count) {
        swal({
            title: "خطا",
            text: "لطفا تعداد مورد نظر را به عددی بیشتر از صفر برسانید",
            icon: "error",
            button: "باشه",
        });
        return;
    }

    $.get("/order/", { product_id: productId, count })
        .then(res => swal({
            title: res.title,
            text: res.message,
            icon: res.status,
            button: res.button,
        }));
}

function deleteFromOrderList(orderItemId) {
    swal({
        title: "آیا مطمئن هستید?",
        text: "شما می خواهید این مورد را حذف کنید!",
        icon: "warning",
        
        buttons: {
            cancel: "انصراف",
            delete: "حذف",
        },
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                $.get("/order/order-item-delete/", {
                    order_item_id: orderItemId
                }).then(res => {
                    console.log(res);
                    if (res.status === 'error') {
                        swal({
                            title: res.title,
                            text: res.message,
                            icon: res.status,
                            button: res.button,
                        })
                    } else {
                        swal("این کالا با موفقیت حذف شد.!", {
                            title: "موفق",
                            icon: "success",
                            button: "باشه",
                        });
                        $("#cart_detail_info").html(res);
                    }
                });
                
            } else {
                swal("انصراف از حذف!", {
                    title: "انصراف",
                    icon: "success",
                    button: "باشه",
                });
            }
        });
    
}


function increaseCountOfProduct(orderItemId) {
    // debugger
    var order_item_id = orderItemId;
    var action = '';
    $.get("/order/order-item-count/", {
        order_item_id,
        action: 'increase'
    }).then(res => {
        if (res.status === 'error') {
            swal({
                title: res.title,
                text: res.message,
                icon: res.status,
                button: res.button,
            })
        } else {
            $("#cart_detail_info").html(res);
        }
    });
}

function decreaseCountOfProduct(orderItemId) {
    var order_item_id = orderItemId;
    var action = '';
    $.get("/order/order-item-count/", {
        order_item_id,
        action: 'decrease'
    }).then(res => {
        if (res.status === 'error') {
            swal({
                title: res.title,
                text: res.message,
                icon: res.status,
                button: res.button,
            })
        } else {
            $("#cart_detail_info").html(res);
        }
        
    });
}



    // document.addEventListener("DOMContentLoaded", function(){
    //     document.querySelector(".post-comment").addEventListener("click", function (e) {
    //         e.preventDefault();
    //         var message = document.querySelector("textarea[name='message']").value;
    //         // استفاده از تابع getCookie برای دریافت CSRF token
    //         var csrfToken = getCookie('csrftoken'); // تغییر اینجا برای استفاده از تابع getCookie
    //         var article_id = "{{article.id}}"
    //         fetch("{% url 'blog_module:submit_comment' %}", {
    //             method: "POST",
    //             headers: {
    //                 "Content-Type": "application/x-www-form-urlencoded",
    //                 "X-CSRFToken": csrfToken,
    //                 "X-Requested-With": "AjaxRequest"
    //             },
    //             body: "message=" + message + "&article_id=" + article_id
    //         })
    //             .then(response => response.json())
    //             .then(data => {
    //                 alert(data.message); // نمایش پیام بازگشتی از سرور
    //                 if (data.success) {
    //                     document.querySelector("textarea[name='message']").value = ''; // پاک کردن فرم
    //                 }
    //             });
    //     });
  //document.querySelector(".replay-comment").addEventListener("click", function(e){
        //e.preventDefault();
        //});
    // });

//     function getCookie(name) {
//         let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//     const cookies = document.cookie.split(';');
//     for (let i = 0; i < cookies.length; i++) {
//       const cookie = cookies[i].trim();
//     if (cookie.substring(0, name.length + 1) === (name + '=')) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//     break;
//       }
//     }
//   }
//     return cookieValue;
// }
