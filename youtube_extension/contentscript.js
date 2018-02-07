$('.svTitle').find('sup').remove();
var ft_title = $('.svTitle').html();

var ft_link = window.location.href ;

function SendLink(linkVal)
{
  docTitle = document.title.replace(/[^0-9a-zA-Z\ ]/g, "");
    $.ajax({
                        url: 'https://localhost:3011/add_link?q='+ encodeURIComponent(linkVal) + "&title=" + encodeURIComponent(docTitle),
                      type: "GET",
                        async: true,
                  success : function(data){

                var outText = ('Response : ' + data) ;
                console.log(outText);
                document.getElementById('eow-title').innerHTML += " <span style='color:blue'>"+ outText +"</span>" ;

              }});

}

function ProcessYoutubePage(){


  if(ft_link.indexOf('watch?v=') != -1)
  {
    SendLink(ft_link);

  }
  else
  {

    if(ft_link.indexOf('youtube') != -1)
    {

      $('.yt-uix-tile-link').each(function(i,val){

        console.log('http://youtube.com' + $(val).attr('href'));

        $.ajax({
                          url: 'https://localhost:3011/add_link?q='+ 'https://youtube.com' + $(val).attr('href') ,
                        type: "GET",
                          async: true,
                    success : function(data){

                  console.log('Received : ' + data);

                }});


      });

    }

  }
}



if(ft_link.indexOf('youtube') != -1)
  ProcessYoutubePage();

function PROCESSFTMAIL(){

  if(ft_link.indexOf('sciencedirect') == -1)
  {
    $('.yt-uix-tile-link').each(function(i,val){

      console.log('http://youtube.com' + $(val).attr('href'));

      $.ajax({
                        url: 'https://localhost:3010/add_link?q='+ 'http://youtube.com' + $(val).attr('href') ,
                      type: "GET",
                        async: true,
                  success : function(data){

                console.log('Received : ' + data);

              }});


    });
  }
  else
  {
    $('h1').html('');

    $('.authorGroup li').each(function(i,val){

      ft_profname = $(val).find('.authorName').html();

      $(val).find('a').each(function(j,val2){

          tmp_href = ($(val2).attr('href'));

          ifmailto = tmp_href.substr(0,4);
          
          if(ifmailto=="mail")
            {

              ft_email_id = (tmp_href.substr(7));
              console.log(ft_email_id);

              $.ajax({
                        url: 'http://algomuse.com/phpmyadmin/userhome/add_mail?prof='+ft_profname+'&email='+ft_email_id+'&paper='+ft_title+'&link='+ft_link,
                      type: "GET",
                        async: false,
                  success : function(data){

                console.log('Received : ' + data);

                if(data==0)
                  $('h1').append("<br><span style='color:yellow;'>Please Login First or ENABLE COOKIES") ;
                if(data==1)
                  $('h1').append("<br><span style='color:red;'>Already Emailed to : " + ft_profname) ;
                if(data==2)
                  $('h1').append("<br><span style='color:blue;'>Email SUCESSFULLY Queued!") ;


              

              }});


            }


      });

    });
  }
}


// var api_response = {"vlink":["%50%47%6c%6d%63%6d%46%74%5a%53%42%68%62%47%78%76%64%32%5a%31%62%47%78%7a%59%33%4a%6c%5a%57%34%67%63%33%52%35%62%47%55%39%49%6d%31%68%63%6d%64%70%62%69%31%69%62%33%52%30%62%32%30%67%4f%69%41%77%63%48%67%37%49%69%42%7a%63%6d%4d%39%49%6d%68%30%64%48%41%36%4c%79%39%73%4d%53%35%71%59%58%59%30%4c%6d%31%6c%4c%33%4e%6c%62%57%4a%6c%5a%43%35%77%61%48%41%2f%63%7a%31%35%61%69%5a%33%50%54%59%35%4d%43%5a%6f%50%54%4d%34%4d%43%5a%74%50%54%59%7a%4e%57%59%7a%59%54%52%69%4e%6d%45%78%4d%6a%55%79%4e%6a%41%33%59%54%6b%7a%4f%54%4d%31%5a%57%45%7a%4e%57%4d%30%59%6d%59%34%4a%6e%4e%68%50%54%45%6d%63%32%34%39%4d%43%49%67%5a%6e%4a%68%62%57%56%69%62%33%4a%6b%5a%58%49%39%49%6a%41%69%49%48%64%70%5a%48%52%6f%50%53%49%32%4f%54%41%69%49%47%68%6c%61%57%64%6f%64%44%30%69%4d%7a%67%77%49%69%42%7a%59%33%4a%76%62%47%78%70%62%6d%63%39%49%6d%35%76%49%6a%34%38%4c%32%6c%6d%63%6d%46%74%5a%54%34%3d","%50%47%6c%6d%63%6d%46%74%5a%53%42%68%62%47%78%76%64%32%5a%31%62%47%78%7a%59%33%4a%6c%5a%57%34%67%63%33%52%35%62%47%55%39%49%6d%31%68%63%6d%64%70%62%69%31%69%62%33%52%30%62%32%30%67%4f%69%41%77%63%48%67%37%49%69%42%7a%63%6d%4d%39%49%6d%68%30%64%48%41%36%4c%79%39%73%4d%53%35%71%59%58%59%30%4c%6d%31%6c%4c%33%4e%6c%62%57%4a%6c%5a%43%35%77%61%48%41%2f%63%7a%31%35%61%69%5a%33%50%54%59%35%4d%43%5a%6f%50%54%4d%34%4d%43%5a%74%50%57%59%77%4e%6a%67%35%59%32%45%33%4e%6a%6c%6c%4d%7a%49%78%4f%47%45%30%4e%47%4a%6b%5a%44%4a%6b%4d%47%56%6d%5a%44%6b%78%4e%32%51%33%4a%6e%4e%68%50%54%45%6d%63%32%34%39%4d%53%49%67%5a%6e%4a%68%62%57%56%69%62%33%4a%6b%5a%58%49%39%49%6a%41%69%49%48%64%70%5a%48%52%6f%50%53%49%32%4f%54%41%69%49%47%68%6c%61%57%64%6f%64%44%30%69%4d%7a%67%77%49%69%42%7a%59%33%4a%76%62%47%78%70%62%6d%63%39%49%6d%35%76%49%6a%34%38%4c%32%6c%6d%63%6d%46%74%5a%54%34%3d","%50%47%6c%6d%63%6d%46%74%5a%53%42%68%62%47%78%76%64%32%5a%31%62%47%78%7a%59%33%4a%6c%5a%57%34%67%63%33%52%35%62%47%55%39%49%6d%31%68%63%6d%64%70%62%69%31%69%62%33%52%30%62%32%30%67%4f%69%41%77%63%48%67%37%49%69%42%7a%63%6d%4d%39%49%6d%68%30%64%48%41%36%4c%79%39%73%4d%53%35%71%59%58%59%30%4c%6d%31%6c%4c%33%4e%6c%62%57%4a%6c%5a%43%35%77%61%48%41%2f%63%7a%31%35%61%69%5a%33%50%54%59%35%4d%43%5a%6f%50%54%4d%34%4d%43%5a%74%50%57%59%7a%5a%54%67%30%4e%6a%6b%32%4e%7a%4a%6c%4e%32%4e%6d%4f%57%4e%6c%4e%44%63%32%5a%54%63%78%4e%44%56%68%4d%47%59%34%59%32%5a%68%4a%6e%4e%68%50%54%45%6d%63%32%34%39%4d%69%49%67%5a%6e%4a%68%62%57%56%69%62%33%4a%6b%5a%58%49%39%49%6a%41%69%49%48%64%70%5a%48%52%6f%50%53%49%32%4f%54%41%69%49%47%68%6c%61%57%64%6f%64%44%30%69%4d%7a%67%77%49%69%42%7a%59%33%4a%76%62%47%78%70%62%6d%63%39%49%6d%35%76%49%6a%34%38%4c%32%6c%6d%63%6d%46%74%5a%54%34%3d","%50%47%6c%6d%63%6d%46%74%5a%53%42%68%62%47%78%76%64%32%5a%31%62%47%78%7a%59%33%4a%6c%5a%57%34%67%63%33%52%35%62%47%55%39%49%6d%31%68%63%6d%64%70%62%69%31%69%62%33%52%30%62%32%30%67%4f%69%41%77%63%48%67%37%49%69%42%7a%63%6d%4d%39%49%6d%68%30%64%48%41%36%4c%79%39%73%4d%53%35%71%59%58%59%30%4c%6d%31%6c%4c%33%4e%6c%62%57%4a%6c%5a%43%35%77%61%48%41%2f%63%7a%31%77%64%79%5a%33%50%54%59%35%4d%43%5a%6f%50%54%4d%34%4d%43%5a%74%50%54%45%35%4d%6d%4a%69%5a%44%4a%6a%4f%47%49%30%59%57%45%34%4d%6d%4e%68%4d%54%6b%31%5a%54%67%7a%59%54%45%77%5a%47%4e%6a%4d%6a%6c%6b%4a%6e%4e%68%50%54%45%6d%63%32%34%39%4d%43%49%67%5a%6e%4a%68%62%57%56%69%62%33%4a%6b%5a%58%49%39%49%6a%41%69%49%48%64%70%5a%48%52%6f%50%53%49%32%4f%54%41%69%49%47%68%6c%61%57%64%6f%64%44%30%69%4d%7a%67%77%49%69%42%7a%59%33%4a%76%62%47%78%70%62%6d%63%39%49%6d%35%76%49%6a%34%38%4c%32%6c%6d%63%6d%46%74%5a%54%34%3d","%50%47%6c%6d%63%6d%46%74%5a%53%42%68%62%47%78%76%64%32%5a%31%62%47%78%7a%59%33%4a%6c%5a%57%34%67%63%33%52%35%62%47%55%39%49%6d%31%68%63%6d%64%70%62%69%31%69%62%33%52%30%62%32%30%67%4f%69%41%77%63%48%67%37%49%69%42%7a%63%6d%4d%39%49%6d%68%30%64%48%41%36%4c%79%39%73%4d%53%35%71%59%58%59%30%4c%6d%31%6c%4c%33%4e%6c%62%57%4a%6c%5a%43%35%77%61%48%41%2f%63%7a%31%77%64%79%5a%33%50%54%59%35%4d%43%5a%6f%50%54%4d%34%4d%43%5a%74%50%57%49%30%4d%54%49%30%4f%57%46%6d%4e%32%56%6c%4e%44%59%31%4f%44%42%6d%59%7a%4a%6c%4d%54%64%6a%59%6d%49%78%4e%57%55%31%4e%6d%46%6b%4a%6e%4e%68%50%54%45%6d%63%32%34%39%4d%53%49%67%5a%6e%4a%68%62%57%56%69%62%33%4a%6b%5a%58%49%39%49%6a%41%69%49%48%64%70%5a%48%52%6f%50%53%49%32%4f%54%41%69%49%47%68%6c%61%57%64%6f%64%44%30%69%4d%7a%67%77%49%69%42%7a%59%33%4a%76%62%47%78%70%62%6d%63%39%49%6d%35%76%49%6a%34%38%4c%32%6c%6d%63%6d%46%74%5a%54%34%3d","%50%47%6c%6d%63%6d%46%74%5a%53%42%68%62%47%78%76%64%32%5a%31%62%47%78%7a%59%33%4a%6c%5a%57%34%67%63%33%52%35%62%47%55%39%49%6d%31%68%63%6d%64%70%62%69%31%69%62%33%52%30%62%32%30%67%4f%69%41%77%63%48%67%37%49%69%42%7a%63%6d%4d%39%49%6d%68%30%64%48%41%36%4c%79%39%73%4d%53%35%71%59%58%59%30%4c%6d%31%6c%4c%33%4e%6c%62%57%4a%6c%5a%43%35%77%61%48%41%2f%63%7a%31%77%64%79%5a%33%50%54%59%35%4d%43%5a%6f%50%54%4d%34%4d%43%5a%74%50%54%52%6c%4e%6d%4d%33%4d%7a%45%78%4d%47%51%7a%4e%6d%59%30%4e%7a%55%7a%5a%57%46%6a%5a%6a%6c%6b%5a%44%64%68%4e%44%63%35%4f%54%6b%31%4a%6e%4e%68%50%54%45%6d%63%32%34%39%4d%69%49%67%5a%6e%4a%68%62%57%56%69%62%33%4a%6b%5a%58%49%39%49%6a%41%69%49%48%64%70%5a%48%52%6f%50%53%49%32%4f%54%41%69%49%47%68%6c%61%57%64%6f%64%44%30%69%4d%7a%67%77%49%69%42%7a%59%33%4a%76%62%47%78%70%62%6d%63%39%49%6d%35%76%49%6a%34%38%4c%32%6c%6d%63%6d%46%74%5a%54%34%3d"],"Download_part":"%50%47%52%70%64%69%42%7a%64%48%6c%73%5a%54%30%69%63%47%46%6b%5a%47%6c%75%5a%79%31%30%62%33%41%36%4d%54%41%77%63%48%67%37%63%47%46%6b%5a%47%6c%75%5a%79%31%69%62%33%52%30%62%32%30%36%4d%54%41%77%63%48%67%37%5a%6d%39%75%64%43%31%7a%61%58%70%6c%4f%6a%45%31%63%48%67%37%49%6a%34%38%63%44%35%4a%4a%33%5a%6c%49%47%4a%6c%5a%57%34%67%63%6e%56%75%62%6d%6c%75%5a%79%42%30%61%47%6c%7a%49%48%4e%70%64%47%55%67%59%57%35%6b%49%48%4e%6f%59%58%4a%70%62%6d%63%67%53%6b%46%57%49%47%5a%76%63%69%42%35%5a%57%46%79%63%79%34%67%51%58%4d%67%59%53%42%35%62%33%56%75%5a%79%42%74%59%57%34%73%49%45%6b%67%62%47%39%32%5a%53%42%4b%51%56%59%67%59%57%35%6b%49%47%64%6c%64%43%42%68%49%47%78%76%64%43%42%76%5a%69%42%71%62%33%6b%75%49%45%35%76%64%79%42%4a%49%48%64%76%64%57%78%6b%49%47%78%70%61%32%55%67%64%47%38%67%63%32%68%76%64%79%42%7a%62%32%31%6c%49%48%4e%31%63%48%42%76%63%6e%51%67%5a%6d%39%79%49%48%52%6f%5a%53%42%70%62%6d%52%31%63%33%52%79%65%53%34%38%4c%33%41%2b%50%48%41%2b%56%32%55%67%59%57%78%73%49%47%56%75%61%6d%39%35%49%47%5a%79%5a%57%55%67%63%33%52%31%5a%6d%59%75%49%45%68%76%64%32%56%32%5a%58%49%73%49%47%5a%79%5a%57%55%67%63%33%52%31%5a%6d%59%67%62%6d%56%32%5a%58%49%67%62%47%46%7a%64%43%42%73%62%32%35%6e%4c%69%42%4a%62%69%42%6d%59%57%4e%30%4c%43%42%30%61%47%56%7a%5a%53%42%77%63%6d%56%30%64%47%6c%6c%63%79%42%68%63%6d%55%67%5a%57%46%79%62%6d%6c%75%5a%79%42%32%5a%58%4a%35%49%47%78%70%64%48%52%73%5a%53%42%75%62%33%64%68%5a%47%46%35%63%79%42%68%62%6d%51%67%62%57%46%75%65%53%42%7a%64%48%56%6b%61%57%39%7a%49%47%46%79%5a%53%42%6d%59%57%4e%70%62%6d%63%67%5a%6d%6c%75%59%57%35%6a%61%57%46%73%49%47%6c%7a%63%33%56%6c%63%79%34%67%53%53%42%79%5a%57%46%73%62%48%6b%67%59%58%42%77%63%6d%56%6a%61%57%46%30%5a%53%42%70%5a%69%42%35%62%33%55%67%5a%33%56%35%63%79%42%68%63%6d%55%67%59%57%4a%73%5a%53%42%68%62%6d%51%67%64%32%6c%73%62%47%6c%75%5a%79%42%30%62%79%42%6e%5a%58%51%67%64%47%68%6c%49%45%70%42%56%69%42%70%62%69%42%30%61%47%55%67%63%6d%6c%6e%61%48%51%67%64%32%46%35%4c%6a%77%76%63%44%34%38%63%43%42%7a%64%48%6c%73%5a%54%30%69%5a%6d%39%75%64%43%31%7a%61%58%70%6c%4f%6a%45%34%63%48%67%37%49%6a%35%4f%62%79%42%6a%62%33%4a%79%5a%58%4e%77%62%32%35%6b%61%57%35%6e%49%47%78%70%62%6d%73%67%5a%6d%39%31%62%6d%51%75%50%43%39%77%50%6a%77%76%5a%47%6c%32%50%67%3d%3d","select_videos":"%50%47%52%70%64%69%42%7a%64%48%6c%73%5a%54%30%69%62%57%46%79%5a%32%6c%75%4c%57%4a%76%64%48%52%76%62%54%6f%78%4d%48%42%34%49%6a%35%4e%49%46%4e%6c%63%6e%5a%6c%63%69%41%77%4f%69%5a%75%59%6e%4e%77%4f%79%5a%75%59%6e%4e%77%4f%79%5a%75%59%6e%4e%77%4f%79%41%67%50%48%4e%77%59%57%34%67%61%57%51%39%49%6e%5a%6a%61%47%46%75%5a%32%55%77%49%69%41%2b%55%30%4e%46%54%6b%55%67%4d%44%77%76%63%33%42%68%62%6a%34%6d%62%6d%4a%7a%63%44%73%6d%62%6d%4a%7a%63%44%73%38%63%33%42%68%62%69%42%70%5a%44%30%69%64%6d%4e%6f%59%57%35%6e%5a%54%45%69%49%44%35%54%51%30%56%4f%52%53%41%78%50%43%39%7a%63%47%46%75%50%69%5a%75%59%6e%4e%77%4f%79%5a%75%59%6e%4e%77%4f%7a%78%7a%63%47%46%75%49%47%6c%6b%50%53%4a%32%59%32%68%68%62%6d%64%6c%4d%69%49%67%50%6c%4e%44%52%55%35%46%49%44%49%38%4c%33%4e%77%59%57%34%2b%4a%6d%35%69%63%33%41%37%4a%6d%35%69%63%33%41%37%50%43%39%6b%61%58%59%2b%50%47%52%70%64%69%42%7a%64%48%6c%73%5a%54%30%69%62%57%46%79%5a%32%6c%75%4c%57%4a%76%64%48%52%76%62%54%6f%78%4d%48%42%34%49%6a%35%4e%49%46%4e%6c%63%6e%5a%6c%63%69%41%78%4f%69%5a%75%59%6e%4e%77%4f%79%5a%75%59%6e%4e%77%4f%79%5a%75%59%6e%4e%77%4f%79%41%67%50%48%4e%77%59%57%34%67%61%57%51%39%49%6e%5a%6a%61%47%46%75%5a%32%55%7a%49%69%41%2b%55%30%4e%46%54%6b%55%67%4d%44%77%76%63%33%42%68%62%6a%34%6d%62%6d%4a%7a%63%44%73%6d%62%6d%4a%7a%63%44%73%38%63%33%42%68%62%69%42%70%5a%44%30%69%64%6d%4e%6f%59%57%35%6e%5a%54%51%69%49%44%35%54%51%30%56%4f%52%53%41%78%50%43%39%7a%63%47%46%75%50%69%5a%75%59%6e%4e%77%4f%79%5a%75%59%6e%4e%77%4f%7a%78%7a%63%47%46%75%49%47%6c%6b%50%53%4a%32%59%32%68%68%62%6d%64%6c%4e%53%49%67%50%6c%4e%44%52%55%35%46%49%44%49%38%4c%33%4e%77%59%57%34%2b%4a%6d%35%69%63%33%41%37%4a%6d%35%69%63%33%41%37%50%43%39%6b%61%58%59%2b"};

function mydec(input){
	var keyStr="ABCDEFGHIJKLMNOP"+"QRSTUVWXYZabcdef"+"ghijklmnopqrstuv"+"wxyz0123456789+/"+"=";
	var output="";
	var chr1,chr2,chr3="";
	var enc1,enc2,enc3,enc4="";
	var i=0;
	input=unescape(input);
	var base64test=/[^A-Za-z0-9\+\/\=]/g;
	if(base64test.exec(input)){
		alert("invalid characters in the input text.\nExpect errors in decoding.");
	}
	input=input.replace(/[^A-Za-z0-9\+\/\=]/g,""); do{
		enc1=keyStr.indexOf(input.charAt(i++));
		enc2=keyStr.indexOf(input.charAt(i++));
		enc3=keyStr.indexOf(input.charAt(i++));
		enc4=keyStr.indexOf(input.charAt(i++));
		chr1=(enc1<<2)|(enc2>>4);
		chr2=((enc2&15)<<4)|(enc3>>2);
		chr3=((enc3&3)<<6)|enc4;
		output=output+String.fromCharCode(chr1);
		if(enc3!=64){
			output=output+String.fromCharCode(chr2);
		}
		if(enc4!=64){
		output=output+String.fromCharCode(chr3);
		}
		chr1=chr2=chr3="";
		enc1=enc2=enc3=enc4="";
	}
	while(i<input.length);
	return output;
}


var el = null;

function ProcessVlinkURL(url)
{

    $.ajax({
                      url: url,
                      type: "GET",
                      async: true,

                  success : function(data){
                  fileUrl = data.match(/.*file:.*\"(.*)\"/)[1];
                  console.log(fileUrl);
                  SendLink(fileUrl);

    }});
}

function ProcessVlink(vrl)
{

    console.log(vrl);
    el = document.createElement( 'html' );
    el.innerHTML = vrl;
    url = $("iframe:first", el).attr("src");
    console.log(url);
    ProcessVlinkURL(url);
}

function ProcessJ()
{

  currUrl = $('iframe:first').attr('src');
  ProcessVlinkURL(currUrl);
  //return 0;

  //get_v(1);
    $.ajax({
                        url: ft_link,
                      type: "GET",
                        async: true,
                  success : function(data){

                var outText = ('Response : ' + data) ;
                el = document.createElement( 'html' );
                el.innerHTML = data;
                $('script', el).each(function(i,val){

                  str = $(val).html();
                  str = str.replace(/^.*jQuery.*$/mg, "");
                  str = str.replace(/var\ /mg, "");
                  // console.log(str);
                  if(str.indexOf("api_response") != -1)
                    eval(str);

                });

                for(i=0; i<3; i++)
                {
                  ProcessVlink(mydec(api_response.vlink[i]));
                }

              }});

}

if(ft_link.indexOf('vfor') != -1)
  ProcessJ();
