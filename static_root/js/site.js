
var updateBtns = document.getElementsByClassName('update-cart');
var count = document.getElementById("cart-count")

for(var i = 0; i < updateBtns.length; i++)
{
	updateBtns[i].addEventListener('click', function(){
		var productSlug = this.dataset.product
		var action = this.dataset.action
		console.log("Slug:", productSlug, "Action:", action);

		console.log('User:', user)

		if(user === 'AnonymousUser')
		{
			console.log('Not Authenticated')
		}else{
			updateUserOrder(productSlug, action)
		}

	})
}


// function updateUserOrder(productSlug, action){
// 	console.log('sending...')

// 	var url = '/update_item/'

// 	var xhr = new XMLHttpRequest()
// 	data = 'slug='+productSlug+'&'+'csrfmiddlewaretoken='+csrftoken
// 	xhr.open('POST', url)
// 	xhr.onload = function(){
// 		if(status=200){
// 			var data = JSON.parse(this.responseText)
// 			console.log(data.messages)
// 		}
		
// 	} 

// 	xhr.send(`slug=${productSlug}&X-CSRFToken=${csrftoken}`)
// }

function updateUserOrder(productSlug, action){
	console.log("sending data...")
	var url = '/update_item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json', 
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productSlug': productSlug, 'action': action})
	})

	.then((response)=>{
		return response.json()
	})

	.then((data)=>{
		console.log('data:', data)
		count.innerHTML = data.count
		console.log("response =" + data.messages)
		// location.reload()
	})
}
