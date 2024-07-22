var updatebtns = document.getElementsByClassName('updatecart')

for (var i = 0; i < updatebtns.length; i++){
    updatebtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)


        console.log('USER:', user)
        if (user === 'AnonymousUser'){
            console.log('user is not real')
        }else{
            updateUserOrder(productId, action)
        } 

        
    })
}

function updateUserOrder(productId, action){
    console.log("user is real")

    var url = '/update_Item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    })
}


//let cartIcon = document.querySelector('.cartIcon');
//let closeCart = document.querySelector('.close');
//let body = document.querySelector('body');

//iconCart.addEventListener('click', () => {
//    body.classList.toggle('showCart')
//})

//closeCart.addEventListener('click', () => {
//    body.classList.toggle('showCart')
//})
