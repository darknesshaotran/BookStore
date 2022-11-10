console.log('part2');
var AddCartBtns = document.getElementsByClassName('update-cart')
for(i=0; i<AddCartBtns.length;i++)
{
    AddCartBtns[i].addEventListener('click',function(){
        var bookId = this.dataset.product
        var action = this.dataset.action
        console.log('bookID:',bookId, 'action:',action)
        console.log('user:',user)
        if(user === 'AnonymousUser')
            console.log('not login yet')
        else 
            updateUserCart(bookId,action)
    })
}
function updateUserCart(bookId,action)
{
    console.log('send data')
    // console.log('send data for',bookId)
    // var url = 'http://localhost:8888/update_item_cart/'
    // fetch("http://localhost:8888/update_item_cart/",{
    //   method: "post",
    //   headers: { "content-Type": "application/json" },
    //   body: JSON.stringify({'bookId':bookId,'action':action})
    // })
    // .then((response)=>{
    //     return response.json()
    // })
    // .then((data)=>{
    //     console.log('data',data)
    // })
}

function a(){
    alert("chưa có")
}

