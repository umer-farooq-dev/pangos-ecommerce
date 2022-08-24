function get_pickup_points(){
	
	var address = $('input[name=address]').val();
    var zipcode = $('input[name=zipcode]').val();
    var city = $('input[name=city]').val();
    var country = $('.countrybox option:selected').text();
	
	$.ajax({
	type: "GET",
	url: "/api/get_pickup_points/",
	data: "zipcode="+zipcode+"&address="+address+"&country="+country+"",
	success: function(msg) {
			
			console.log(msg);
			
			var stringinfo = '';
			var counter = 0;
			
			var pickup_address = $('input[name=pickup_address]').val();
			var pickupid = parseInt($('input[name=pickup_id]').val());
			var pickupname = '';
			var pickupzipcode = '';
			var pickupcity = '';
			var pickupcountry = '';
			
			console.log(pickupid);
			
			
			/*stringinfo = stringinfo+'<div class="delivery-box-picker" pickup-id="home">\
			      <div class="radio"><input type="radio" class="pickup_home"  /></div>\
			      <div class="info"><span class="pickup_name_home">Hjemmelevering</span> - <span class="pickup_address_home">'+address+'</span>, <span class="pickup_zipcode_home">'+zipcode+'</span> <span class="pickup_city_home">'+city+'</span> <span class="pickup_country_home" style="display: none">Danmark</span></span><br /><span class="km_calc">+39 kr</span></div>\
			      <div class="clearfix"></div>\
		      </div>';*/
			
			$(msg.output).each(function(i,v){
				
				if(counter == 0){
					var deliveryactive = 'active';
					var deliverychecked = 'checked';
					pickupid = v.id;
					pickup_address = v.address;
					
					pickup_name = v.name;
					pickup_zipcode = v.zipcode;
					pickup_city = v.city;
					pickup_country = v.country;
					
				}else{
					var deliveryactive = '';
					var deliverychecked = '';
				}
				
				var mtokm = parseInt(v.distance)/1000;
				var mtokm = parseFloat(mtokm).toFixed(2);
				
				stringinfo = stringinfo+'<div class="delivery-box-picker '+deliveryactive+'" pickup-id="'+v.id+'">\
			      <div class="radio"><input type="radio" class="pickup_'+v.id+'" '+deliverychecked+' /></div>\
			      <div class="info"><span class="pickup_name_'+v.id+'">'+v.name+'</span> - <span class="pickup_address_'+v.id+'">'+v.address+'</span>, <span class="pickup_zipcode_'+v.id+'">'+v.zipcode+'</span> <span class="pickup_city_'+v.id+'">'+v.city+'</span> <span class="pickup_country_'+v.id+'" style="display: none">'+v.country+'</span></span><br /><span class="km_calc">Gratis - '+mtokm+' km fra din adresse</span></div>\
			      <div class="clearfix"></div>\
		      </div>';
		      
		      	counter++;
				
			});
			
			stringinfo = stringinfo+'<div class="delivery-box-picker homedelivery" pickup-id="home">\
			      <div class="radio"><input type="radio" class="pickup_home" /></div>\
			      <div class="info"><span class="pickup_name_home">Hjemmelevering</span> - <span class="pickup_address_home">'+address+'</span>, <span class="pickup_zipcode_home">'+zipcode+'</span> <span class="pickup_city_home"></span> <span class="pickup_country_home" style="display: none">Danmark</span></span><br /><span class="km_calc">+29 kr for hjemmelevering</span></div>\
			      <div class="clearfix"></div>\
		      </div>';
			
			$('input[name=pickup_id]').val(pickupid);
			$('input[name=pickup_address]').val(pickup_address);
			
			$('input[name=pickup_name]').val(pickup_name);
			$('input[name=pickup_city]').val(pickup_city);
			$('input[name=pickup_zipcode]').val(pickup_zipcode);
			$('input[name=pickup_country]').val(pickup_country);
			
			$('.delivery-wrapper').html(stringinfo);
			$('.no-delivery-found').hide();
			
			homedelivery();
		}
	});
}

function homedelivery(){
	$(".delivery-box-picker").click(function() {
		
		var ptype = $(this).attr('pickup-id');
				
		var pid = $('input[name=payid]').val();
		var newamount = $('input[name=basicprice]').val();
		//if($('input[name=payid_home]').val() == ''){
			
		if(ptype == 'home'){
			$('.delivery_info_home').show();
			$('.delivery_info_free').hide();
			
			$('.price-without-home-shipping').hide();
			$('.price-with-home-shipping').show();
			
		}else{
			$('.delivery_info_home').hide();
			$('.delivery_info_free').show();
			
			$('.price-without-home-shipping').show();
			$('.price-with-home-shipping').hide();
		}
			
		$.ajax({
		  type: "POST",
		  url: "/api/update_intent",
		  data: "pid="+pid+"&newamount="+newamount+"&ptype="+ptype,
		  success: function(msg) {
			  $('input[name=payid_home]').val(msg);
		  }
		});
		//}
	});
}

$(document).ready(function() {
    $(".not-you").click(function() {
	    $('html, body').animate({
	        scrollTop: $(".seemoreapartments").offset().top
	    }, 2000);
	    
	    return false;
	});  
	
	$('.create-intent').click(function(){
		
		var email = $('input[name=email]').val();
		var pickupid = $('input[name=pickup_id]').val();
		
		$.ajax({
		  type: "GET",
		  url: "/api/create_intent",
		  data: "email="+email+"&pickupid="+pickupid,
		  success: function(msg) {
			  $('input[name=payid]').val(msg.payment_id);
			  $('.completePurchase').attr('data-secret',msg.client_secret);
			  $('input[name=customer_id]').val(msg.customer_id);
		  }
		});
		
	});
	
	$('.next-step-flow').click(function(){
	    
	    var error = false;
	    
	    var firstname = $('input[name=firstname]').val();
	    var lastname = $('input[name=lastname]').val();
	    var address = $('input[name=address]').val();
	    var zipcode = $('input[name=zipcode]').val();
	    var city = $('input[name=city]').val();
	    var number = $('input[name=number]').val();
	    var email = $('input[name=email]').val();
	    var subscription_check_first = $('input[name=subscription_check_first]').val();
	    
	    if(firstname == ''){
		    $('input[name=firstname]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=firstname]').removeClass('error');
	    }
	    
	    if(lastname == ''){
		    $('input[name=lastname]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=lastname]').removeClass('error');
	    }
	    
	    if(address == ''){
		    $('input[name=address]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=address]').removeClass('error');
	    }
	    
	    if(zipcode == ''){
		    $('input[name=zipcode]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=zipcode]').removeClass('error');
	    }
	    
	    if(city == ''){
		    $('input[name=city]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=city]').removeClass('error');
	    }
	    
	    if(number == ''){
		    $('input[name=number]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=number]').removeClass('error');
	    }
	    
	    if(email == ''){
		    $('input[name=email]').addClass('error');
		    error = true;
	    }else{
		    $('input[name=email]').removeClass('error');
	    }
	    
	    if(!$('input[name=subscription_check_first]').is(':checked')){
		    $('input[name=subscription_check_first]').addClass('error');
		    error = true;
		    var condition_error = true;
	    }else{
		    $('input[name=subscription_check_first]').removeClass('error');
		    var condition_error = false;
	    }
	    
	    if(!error){
		    console.log('next');
		    $('.step-box-flow-one').fadeOut('fast');
		    $('.step-box-flow-two').show();
		    
		    $('.step-box-flow-two').show();
		    $('.delivery-payment-top-box.first').removeClass('active');
		    $('.delivery-payment-top-box.second').addClass('active');
		    
		    setTimeout(function(){
			   $("html, body").animate({ scrollTop: $('#step-box-flow-two').offset().top }, 200); 
			}, 1000);
		    
	    }else{
		    if(condition_error){
			    $('.condition-error').show();
		    }else{
			    $('.condition-error').hide();
		    }
	    }
	    		
		return false;
    });
    
    $('.delivery-payment-top-box.first, .goback').click(function(){
	   
	   $('.step-box-flow-two').fadeOut('fast');
	   $('.step-box-flow-one').show();
	   
	   $('.delivery-payment-top-box.first').addClass('active');
	   $('.delivery-payment-top-box.second').removeClass('active');
	    
    });

	$('.smegam').mouseenter(function () {
	   
	   var id = $(this).attr('data-id');
	   $('.cat-sub').hide();
	   $('.mega-menu').addClass('over');
	   $('.cat-sub-'+id).show();
	   
       $('.mega-menu').show();
    });
    
    $('.hmegam').mouseenter(function () {
	   
	   $('.mega-menu').hide();
	   $('.mega-menu').removeClass('over');
    });
    
    if($('.complete-order input[name=address]').length){
		var address = $('.complete-order input[name=address]').val();
    	var zipcode = $('.complete-order input[name=zipcode]').val();
    	
    	if(address && zipcode){
    	
	    	get_pickup_points();
		
		}
	}
	
	$( "input[name=address], input[name=zipcode]" ).focusout(function() {
    	var address = $('input[name=address]').val();
    	var zipcode = $('input[name=zipcode]').val();
    	
    	if(address && zipcode){
    	
	    	get_pickup_points();
		
		}
    	
  	});
  	
  	
  	$(document).on("click",".delivery-box-picker",function(){
		var pickid = $(this).attr('pickup-id');
		var pickaddress = $('.pickup_address_'+pickid).html();
		var pickname = $('.pickup_name_'+pickid).html();
		var pickcity = $('.pickup_city_'+pickid).html();
		var pickzipcode = $('.pickup_zipcode_'+pickid).html();
		var pickcountry= $('.pickup_country_'+pickid).html();
		
		$('.delivery-box-picker').removeClass('active');
		
		$('.delivery-box-picker input[type=radio]').prop('checked',false);
		$('.pickup_'+pickid).prop('checked',true);
		
		$('input[name=pickup_id]').val(pickid);
		$('input[name=pickup_address]').val(pickaddress);
		$('input[name=pickup_name]').val(pickname);
		$('input[name=pickup_city]').val(pickcity);
		$('input[name=pickup_zipcode]').val(pickzipcode);
		$('input[name=pickup_country]').val(pickcountry);
		
		if(pickid == 'home'){
			$('.with_discount_box').show();
			$('.non_discount_box').hide();
		}else{
			$('.with_discount_box').hide();
			$('.non_discount_box').show();
		}
		
		$(this).addClass('active');
		
	});
    
    $('.mega-menu').mouseenter(function () {
	   $(this).addClass('over');
       $('.mega-menu').show();
    });

    $('.smegam').mouseleave(function () {
	    setTimeout(function () {
		    if($('.mega-menu').hasClass('over')){
			    
		    }else{
	        	$('.mega-menu').hide();
	        }
	    }, 5000);
	}).mouseleave();
	
	$('.mega-menu').mouseleave(function () {
	    setTimeout(function () {
		    $('.mega-menu').hide();
		    $('.mega-menu').removeClass('over');
	    }, 500);
	}).mouseleave();

	$('[data-toggle="tooltip"]').tooltip();
	
	if($('.payments-received').length){
		$.ajax({
		  type: "POST",
		  url: "/user/charges",
		  data: "",
		  success: function(msg) {
			  
			var string = '';
			
			if(msg.length == 0){
				string = string+'<tr>\
			    <td colspan="4" align="center">Ingen betalinger fundet</td>\
			    </tr>';
			}else{
			
			    $(msg).each(function(i,k){
				    string = string+'<tr>\
				    <td>'+k.created+'</td>\
				    <td>'+k.amount+' kr</td>\
				    <td>'+k.type+'</td>\
				    <td><a href="/user/invoice/'+k.id+'">Hent faktura</a></td>\
				    </tr>';
			    });
		    
		    }
			
			$('.payments-received').html(string);
			
		  }
		});
	}
	
	if($('#payment-form input[name=email]').length){
		var $email = $('#payment-form input[name=email]').val();
		if($email != ''){
	    if(validateEmail($email)){
		    // check if old customer
		    $.ajax({
				type: "POST",
				url: "/checkout/validate_user_type",
				data: "email="+$email+"",
				success: function(msg) {
					if(msg == 1){
						// show addon fee
						if($('.bought-before-box').length){
							$('.bought-before-box').show();
							$('.new-customer-box').hide();
						}
					}else{
						// hide addon fee
						$('.bought-before-box').hide();
						$('.new-customer-box').show();
					}
				}
			});
	    }
	    }
	}
	
	$('#payment-form input[name=email]').first().keyup(function () {
		if($('#payment-form input[name=email]').val() != ''){
	    var $email = this.value;
	    if(validateEmail($email)){
		    // check if old customer
		    $.ajax({
				type: "POST",
				url: "/checkout/validate_user_type",
				data: "email="+$email+"",
				success: function(msg) {
					if(msg == 1){
						// show addon fee
						if($('.bought-before-box').length){
							$('.bought-before-box').show();
							$('.new-customer-box').hide();
						}
						
						$('.prev-user-bought-text').show();
						$('.new-user-bought-text').hide();
						
					}else{
						// hide addon fee
						$('.bought-before-box').hide();
						$('.new-customer-box').show();
						
						$('.prev-user-bought-text').hide();
						$('.new-user-bought-text').show();
					}
				}
			});
	    }
	    }
	});
	
	$('.cart-resume-open').click(function(){
		
		$('.cart-resume').slideToggle('fast');
		return false;
		
	});
		
	$('.setAgreeCookie').click(function(){
		Cookies.set('agreedterms', '1', { expires: 1 });
		$('#popup').modal('hide');
		return false;
	});
	
	$('.confirm').click(function(){
		
		if(!confirm('Er du sikker?')){
			return false;
		}
		
	});
	
	$('.mobileSub').click(function(e){
				
		if(e.currentTarget.className == 'pull-right mobileSub'){
			
			var id = $(this).attr('data-id');
			
			$('.dropdown-menu').not('.submenu_'+id).hide();
			
			if($('.submenu_'+id).is(":visible")){
				$('.submenu_'+id).hide();
			}else{
				$('.submenu_'+id).show();
			}
			
			return false;
		}
	});
	
	
	$('.discountBox').click(function(){
		$('.showDiscountBox').slideToggle('fast');
		return false;
	});
	
	$('.chooseVariant').change(function(){
		var inventory = $('.chooseVariant option:selected').attr('data-inventory');
		if(inventory == 0){
			$('.not-inventory-div').show();
			$('input[name=add_to_cart]').hide();
		}else{
			$('.not-inventory-div').hide();
			$('input[name=add_to_cart]').show();
		}
		
	});
	
	$('input[name=buy_type]').click(function(){

		$('input[name=buy_type]').not(this).attr('checked',false);
		
	});
	
	$('.imagebox .position').click(function(){
		
		$('.imagebox .top').val(0);
		
		$('.imagebox .position').css('background','#6e6e6e');
		$(this).css('background','#61ac1e');
		
		var imageid = $(this).attr('imageid');
		$('.top_'+imageid).val(1);
		
	});
	
	$('.imagebox .delete').click(function(){
		
		$(this).closest('.imagebox').remove();
		
	});
	
	
	$('.previewImages').click(function(){
		
		$('.previewImages').css('opacity','0.5');
		$(this).css('opacity','1');
		
		$('.big-apartment-big').attr('src',$(this).attr('src'));
		
	});
	
	$('.extraImages').click(function(){
		
		var attr = $(this).attr('src');
		
		$('.extraImages').css('opacity',0.5);
		
		$(this).css('opacity',1);
		
		$('.bigImage').attr('src',attr);
		
	});
	
	$('.open-sidemenu, .overlay').on('click', function() {
	  $('.side-menu').toggleClass('open');
	  $('.overlay').toggleClass('visible');
	  return false;
	});
	
	$('.opensub').click(function(){
		
		var id = $(this).attr('data-id');
		$('.mobile-nav').hide();
		$('.cat-m-sub-'+id).show();
		
		return false;
		
	});
	
	if($('input[name=address]').length){
		var address = $('input[name=address]').val();
    	var zipcode = $('input[name=zipcode]').val();
    	
    	if(address && zipcode){
    	
	    	get_pickup_points();
		
		}
	}
	
	$( "input[name=address], input[name=zipcode]" ).focusout(function() {
    	var address = $('input[name=address]').val();
    	var zipcode = $('input[name=zipcode]').val();
    	
    	if(address && zipcode){
    	
	    	get_pickup_points();
		
		}
    	
  	});
  	
  	$(document).on("click",".delivery-box-picker",function(){
		var pickid = $(this).attr('pickup-id');
		var pickaddress = $('.pickup_address_'+pickid).html();
		var pickname = $('.pickup_name_'+pickid).html();
		var pickcity = $('.pickup_city_'+pickid).html();
		var pickzipcode = $('.pickup_zipcode_'+pickid).html();
		var pickcountry= $('.pickup_country_'+pickid).html();
		
		$('.delivery-box-picker').removeClass('active');
		
		$('.delivery-box-picker input[type=radio]').prop('checked',false);
		$('.pickup_'+pickid).prop('checked',true);
		
		$('input[name=pickup_id]').val(pickid);
		$('input[name=pickup_address]').val(pickaddress);
		$('input[name=pickup_name]').val(pickname);
		$('input[name=pickup_city]').val(pickcity);
		$('input[name=pickup_zipcode]').val(pickzipcode);
		$('input[name=pickup_country]').val(pickcountry);
		
		if(pickid == 'home'){
			$('.with_discount_box').show();
			$('.non_discount_box').hide();
			$('.delivery-amount').html(29);
			
			var normalprice = parseFloat($('.collect-price').attr('data-standard'));
			var normalprice = normalprice+29;
			$('.collect-price').html(normalprice+' kr');
		}else{
			$('.with_discount_box').hide();
			$('.non_discount_box').show();
			$('.delivery-amount').html(0);
			
			var normalprice = parseFloat($('.collect-price').attr('data-standard'));
			$('.collect-price').html(normalprice+' kr');
		}
		
		$(this).addClass('active');
		
	});
	
	$('.goback-menu').click(function(){
		
		$('.cat-m-sub').hide();
		$('.mobile-nav').show();
		
		return false;
		
	});
	
});

function stripeResponseHandler(status, response) {
  // Grab the form:
  var $form = $('#payment-form');

  if (response.error) { // Problem!

    // Show the errors on the form:
    $form.find('.payment-errors').text(response.error.message);
    $form.find('.submit').prop('disabled', false); // Re-enable submission

  } else { // Token was created!

    // Get the token ID:
    var token = response.id;

    // Insert the token ID into the form so it gets submitted to the server:
    $form.append($('<input type="hidden" name="stripeToken">').val(token));

    // Submit the form:
    $form.get(0).submit();
  }
};

function validateEmail(email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    if (!emailReg.test(email)) {
        return false;
    } else {
        return true;
    }
}