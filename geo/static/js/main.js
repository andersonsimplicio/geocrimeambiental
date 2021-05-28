
function ObterToken(){
    let csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method){
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajax(
        {
            beforesend:function(xhr,settings){
                if(!csrfSafeMethod(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader('X-CSRFToken',csrftoken);
                }
            },
        }
    );
    return csrftoken
}

function add_table(assunto){
    let tabela = document.querySelector("#tbody_subjects");
    let tr = document.createElement('tr');
    let td = document.createElement('td');
    let div = document.createElement('div');
    let td2 = document.createElement('td');
    let div2 = document.createElement('div');
    div.className="align-middle";
    div.textContent=assunto.codigo;
    td.appendChild(div);
    tr.appendChild(td);
    div2.textContent=assunto.descricao;
    td2.appendChild(div2);
    tr.appendChild(td2);
    tabela.appendChild(tr);
}

function search_subjects(){
    let token = ObterToken();
    bt =document.querySelector("#buscar");
    let assunto = document.querySelector('#search_id').value;
    
    let path = bt.dataset.url;

    $.ajax(
        {
            type:'POST',
            url:path,
            data:{  
                    'csrfmiddlewaretoken':token,
                    'assunto':assunto,
                },
                cache: false,
                success: function(resp){
                   
                    const data = JSON.parse(JSON.stringify(resp.assuntos));
                    console.log(typeof(data));
                    if(Array.isArray(data)){
                       data.forEach(assunto=>{
                           console.log(assunto.codigo);
                           add_table(assunto);
                       })

                    }else{
                        console.log("Não temos um array")
                    }
                    // d = JSON.parse(JSON.stringify(d['assuntos']));
                    // returnData(d);
                }
    });
}
const btn =document.querySelector("#buscar"); 
btn.addEventListener('click',search_subjects);