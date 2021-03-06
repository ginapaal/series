var integer = 0;
var endPoint = 15;

function table() {
    $.getJSON('/table_data', function(data){
        for (var i = integer; i< endPoint; i++) {
            $('.tableBody').append(`<tr class="tableRow">
                                    <td><a href="/detailed/${data[i]['id']}" class="detailed-link" data-id="${data[i]['id']}">${data[i]['title']}</a></td>
                                    <td>${data[i]['year']}</td>
                                    <td>${data[i]['runtime']}</td>
                                    <td class="genres_data">${data[i]['genres']}</td>
                                    <td>${data[i]['rating']}</td>
                                    <td><a href = "${data[i]['trailer']}"> ${data[i]['title']} trailer </td>
                                    <td><a href = "${data[i]['homepage']}"> Homepage of ${data[i]['title']}</td>
                                    <td class="action-column">
                                        <a href="/edit/${data[i]['id']}"><button type="button" class="icon-button edit-button" data-id="${data[i]['id']}"><i class="fa fa-edit fa-fw"></i></button></a>
                                        <a href="/delete/${data[i]['id']}"><button type="button" class="icon-button delete-button" data-id="${data[i]['id']}"><i class="fa fa-trash fa-fw"></i></button></a>
                                    </td>
                                    </tr>`);  
        }
        
        
        $('#seriesTable').tablesorter();

        var table = $('.tableBody');
        var counter = 0;

        table.find('tr').click(function(){
            var title = $(this).find('td:first').text();
            var itemId = $(this).find('a').data('id');
            
            $.ajax({
            url: `/detailed/${itemId}`,
            method: "POST",
            data: {
                itemId: itemId
            },
            success: function(){
                console.log(itemId);
            }
            });
        });

    });
    
}

function pagination() {
    var num1 = $('#1');
    var num2 = $('#2');
    num1.click(function(){
        num2.removeClass('active');
        num1.addClass('active');
        $("#seriesTable").find("tr:gt(0)").remove();
        integer = 0;
        table();
    });

    num2.click(function(){
        num1.removeClass('active');
        num2.addClass('active');
        $("#seriesTable").find("tr:gt(0)").remove();
        integer += 15;
        endPoint= 20;
        table()
    });
}

function detailedPage() {
    var trailerButton = $('.trailer_button');
    var count = 0;
    trailerButton.click(function() {
        count ++;
        openCloseDivs(count, $('.trailer'));
    });

    var seasonButton = $('.seasons_button');
    var seasonCount = 0;
    seasonButton.click(function() {
        seasonCount ++;
        if (seasonCount % 2 === 1){
            $('.seasons-details, .seasons').show(600);
        } else {
            $('.seasons-details').hide(600);
        }

    });
}

function fancyThead() {
    var thead = $('.thead');

    thead.on('mouseover', function(){
        thead.css('cursor', 'pointer');
    });
}

function seasonCard(itemId) {
    var clickLink = $('.click-link');
    var clickCount = 0;
    var episodeCount = 0;
    

    clickLink.on('mouseover', function() {
        clickLink.css('cursor', 'pointer');
    });

    clickLink.click(function(){
        clickCount ++;
        var seasonNumber = $(this).data('id');
        var overview = $('*[data-seasonid="'+ seasonNumber +'"]');
        
        if (clickCount % 2 === 1){
            overview.show(600);
        } else {
            $('.seasons').find('div:first').hide(600);
            overview.find('div:first').hide(600);
        }

    });

    $('.episodes').click(function() {
        episodeCount ++;
        var seasonNum= $(this).data('buttonid');
        var episodeOfSeason = $('*[data-episodeid="'+ seasonNum +'"]');
        openCloseDivs(episodeCount, episodeOfSeason);
    });
}


function overViewButton() {
    var oWButton = $('.write_overview');
    var oWCount=0;
    var div = $('.overview_input');
    oWButton.click(function(){
        oWCount ++;
        openCloseDivs(oWCount, div);
    });
}

function openCloseDivs(counterType, selector){
    if (counterType % 2 === 1){
        selector.show(600);
    } else {
        selector.hide(600);
    }
}

function restoreOrDelete() {
    $('.bt_restore, .bt_delete_again').click(function() {
        deletedShowId = $(this).data('id');
    });
    
    $('.bt_restore').click(function() {
        $.ajax({
            url: `/deleted/restore`,
            method: 'POST',
            data: {
                deletedShowId: deletedShowId
            },
            success: function() {
                console.log(deletedShowId);
            }
        });
    });
    
}


function main() {
    table();
    pagination();
    detailedPage();
    fancyThead();
    seasonCard();
    overViewButton();
    restoreOrDelete();
}

$(document).ready(main);