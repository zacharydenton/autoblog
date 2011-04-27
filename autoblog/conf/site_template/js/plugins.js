
// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  arguments.callee = arguments.callee.caller;  
  if(this.console) console.log( Array.prototype.slice.call(arguments) );
};
// make it safe to use console.log always
(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();)b[a]=b[a]||c})(window.console=window.console||{});

// Simulates PHP's date function
Date.prototype.format=function(format){var returnStr='';var replace=Date.replaceChars;for(var i=0;i<format.length;i++){var curChar=format.charAt(i);if(i-1>=0&&format.charAt(i-1)=="\\"){returnStr+=curChar;}else if(replace[curChar]){returnStr+=replace[curChar].call(this);}else if(curChar!="\\"){returnStr+=curChar;}}return returnStr;};Date.replaceChars={shortMonths:['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],longMonths:['January','February','March','April','May','June','July','August','September','October','November','December'],shortDays:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],longDays:['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],d:function(){return(this.getDate()<10?'0':'')+this.getDate();},D:function(){return Date.replaceChars.shortDays[this.getDay()];},j:function(){return this.getDate();},l:function(){return Date.replaceChars.longDays[this.getDay()];},N:function(){return this.getDay()+1;},S:function(){return(this.getDate()%10==1&&this.getDate()!=11?'st':(this.getDate()%10==2&&this.getDate()!=12?'nd':(this.getDate()%10==3&&this.getDate()!=13?'rd':'th')));},w:function(){return this.getDay();},z:function(){var d=new Date(this.getFullYear(),0,1);return Math.ceil((this-d)/86400000);},W:function(){var d=new Date(this.getFullYear(),0,1);return Math.ceil((((this-d)/86400000)+d.getDay()+1)/7);},F:function(){return Date.replaceChars.longMonths[this.getMonth()];},m:function(){return(this.getMonth()<9?'0':'')+(this.getMonth()+1);},M:function(){return Date.replaceChars.shortMonths[this.getMonth()];},n:function(){return this.getMonth()+1;},t:function(){var d=new Date();return new Date(d.getFullYear(),d.getMonth(),0).getDate()},L:function(){var year=this.getFullYear();return(year%400==0||(year%100!=0&&year%4==0));},o:function(){var d=new Date(this.valueOf());d.setDate(d.getDate()-((this.getDay()+6)%7)+3);return d.getFullYear();},Y:function(){return this.getFullYear();},y:function(){return(''+this.getFullYear()).substr(2);},a:function(){return this.getHours()<12?'am':'pm';},A:function(){return this.getHours()<12?'AM':'PM';},B:function(){return Math.floor((((this.getUTCHours()+1)%24)+this.getUTCMinutes()/60+this.getUTCSeconds()/3600)*1000/24);},g:function(){return this.getHours()%12||12;},G:function(){return this.getHours();},h:function(){return((this.getHours()%12||12)<10?'0':'')+(this.getHours()%12||12);},H:function(){return(this.getHours()<10?'0':'')+this.getHours();},i:function(){return(this.getMinutes()<10?'0':'')+this.getMinutes();},s:function(){return(this.getSeconds()<10?'0':'')+this.getSeconds();},u:function(){var m=this.getMilliseconds();return(m<10?'00':(m<100?'0':''))+m;},e:function(){return"Not Yet Supported";},I:function(){return"Not Yet Supported";},O:function(){return(-this.getTimezoneOffset()<0?'-':'+')+(Math.abs(this.getTimezoneOffset()/60)<10?'0':'')+(Math.abs(this.getTimezoneOffset()/60))+'00';},P:function(){return(-this.getTimezoneOffset()<0?'-':'+')+(Math.abs(this.getTimezoneOffset()/60)<10?'0':'')+(Math.abs(this.getTimezoneOffset()/60))+':00';},T:function(){var m=this.getMonth();this.setMonth(0);var result=this.toTimeString().replace(/^.+ \(?([^\)]+)\)?$/,'$1');this.setMonth(m);return result;},Z:function(){return-this.getTimezoneOffset()*60;},c:function(){return this.format("Y-m-d\\TH:i:sP");},r:function(){return this.toString();},U:function(){return this.getTime()/1000;}};


// place any jQuery/helper plugins in here, instead of separate, slower script files.
jQuery.githubUser = function(username, callback) {
  jQuery.getJSON("http://github.com/api/v1/json/" + username + "?callback=?", callback);
}
 
jQuery.fn.loadRepositories = function(username) {
  this.html("<span>Querying GitHub for repositories...</span>");
 
  var target = this;
  $.githubUser(username, function(data) {
    var repos = data.user.repositories;
    sortByNumberOfWatchers(repos);
 
    var list = $('<dl/>');
    target.empty().append(list);
    $(repos).each(function() {
      list.append('<dt><a href="'+ this.url +'">' + this.name + '</a></dt>');
      list.append('<dd>' + this.description + '</dd>');
    });
  });
 
  function sortByNumberOfWatchers(repos) {
    repos.sort(function(a,b) {
      return b.watchers - a.watchers;
    });
  }
};

jQuery.fn.latestCommits = function(username, repository, limit) {
    this.html("<span>Querying GitHub for latest commits...</span>");

    var target = this;
    jQuery.getJSON("http://github.com/api/v2/json/commits/list/" + username + "/" + repository + "/master?callback=?", function(data) {
        var commits = data.commits;
        if (limit) {
            commits = commits.slice(0, limit);
        }
        var list = $('<dl/>');
        target.empty().append(list);
        $(commits).each(function() {
            var authored = new Date(this.authored_date);
            list.append('<dt><a href="https://github.com' + this.url + '">' + authored.format('M jS, Y (G:i)') + '</a></dt>');
            list.append('<dd>' + this.message + '</dd>');
        });
    });
};

(function ($) {

    /* ######################### Recent Tracks Class definition ################################# */

    var recentTracksClass = function (elem, options) {

        var $myDiv   = elem,
            lasttime = 0,
            refresh  = parseInt(options['refresh'], 10),
            $list,
            timer,
            lastCurrentPlaying = false;
        
        if (refresh > 0) {
            timer = window.setInterval(function(){ 
                doLastPlayedStuff();
            }, refresh * 1000);
        }
        
        doLastPlayedStuff();
    
        function doLastPlayedStuff() {

            // remove error div if exists
            $myDiv.children('.error').remove();

            //create URL
            var url = 'http://ws.audioscrobbler.com/2.0/?callback=?',
                params = {
                    method:  "user.getrecenttracks",
                    format:  "json",
                    limit:   options.limit,
                    user:    options.username,
                    api_key: options.apikey
                };
            
            //sending request
            $.getJSON(url, params, function(data) {
                
                var foundCurrentPlayingTrack = false;
                
                //check for errors
                if ( !data || !data.recenttracks ) {
                    return error('Username "' + options.username + '" does not exist!');
                } else if( !data.recenttracks.track ) {
                    return error('"' + options.username + '" has no tracks to show!');
                }
                
                //create ul if not exists
                $list = $myDiv.children('ul');
                if (!$list.length) {
                    $list = $("<ul>").appendTo( $myDiv.html('') );
                }
                
                //walk through each Track - reversed to fill up list from latest to newest
                $(data.recenttracks.track.reverse()).each(function(i, track) {
                    var tracktime, tracknowplaying, ts, listitem, dateCont;

                    //getting timestamp from latestentry
                    if(track.date && track.date.uts > lasttime) {
                        tracktime = parseInt(track.date.uts, 10);
                    }
                    
                    //check if entry is currently playing
                    if( track['@attr'] && track['@attr'].nowplaying == 'true' ) {
                        foundCurrentPlayingTrack = true;
                        if( lastCurrentPlaying.name != track.name ) {
                            lastCurrentPlaying = track;
                            tracknowplaying = true;
                            //remove old nowplaying entry
                            $list.children('li.nowplaying').remove();
                        }
                    }
                    
                    if(tracktime > lasttime || (tracknowplaying && options.shownowplaying)) {
                        
                        // ------------ create list item -----------
                        listitem = $( "<li>", { 
                            // add nowplaying class
                            className: tracknowplaying ? "nowplaying" : ""
                        });
                        
                        // ----------------- IMAGE -----------------
                        if (options.cover) {
                            if (track.image[2]['#text']) {
                                $("<img>", {
                                    src: track.image[2]['#text'],
                                    width: "64"
                                }).appendTo(listitem);
                            }
                        }
                        
                        // ---------------- DATE -------------------
                        if (options.datetime) {
                            
                            if (tracknowplaying) {
                                dateCont = 'now';
                            } else {
                                ts = new Date(tracktime * 1000);
                                dateCont = makeTwo(ts.getDate())+'.'+makeTwo(ts.getMonth()+1)+' - '+makeTwo(ts.getHours())+':'+makeTwo(ts.getMinutes());
                            }
                            
                            $("<div>", {
                                className: "date",
                                html: dateCont
                            }).appendTo(listitem);
                        }
                        
                        
                        // ----------------- TRACK -----------------
                        $("<div>", {
                            className: 'track',
                            html: track.name
                        }).appendTo(listitem);
                        
                        // ---------------- ARTIST -----------------
                        $("<div>", {
                            className: 'artist',
                            html: track.artist['#text']
                        }).appendTo(listitem);
                        
                        // ---------------- ALBUM ------------------
                        $("<div>", {
                            className: 'album',
                            html: track.album['#text']
                        }).appendTo(listitem);
                        
                        //add listitem to list
                        $list.prepend(listitem);
                        
                        if(!tracknowplaying) {
                            lasttime = tracktime;
                        }
                    }
                    
                });
                
                if( !foundCurrentPlayingTrack ) {
                    lastCurrentPlaying = false;
                    //remove old nowplaying entry
                    $list.children('li.nowplaying').remove();
                }
                
                //throw old entries away
                if (options.grow === false) {
                    while($list.children().length > options.limit) {
                        $list.children('li').last().remove();
                    }
                }
            
            });

        }
        
        function makeTwo(i) {
            return i < 10 ? '0' + i : i;
        }
        
        function error( message ) {
             $("<p>", {
                    className: "error",
                    html: message
                }).appendTo($myDiv);
                window.clearInterval(timer);
        }

    };

    /* ######################## Recent Tracks Class ends here ################################# */





    /* ######################### Now Playing Class definition ################################# */

    var nowPlayingClass = function (elem, options) {

        var $myDiv   = elem,
            refresh  = parseInt(options['refresh'], 10),
            timer,
            lastCurrentPlaying = false;
        
        if (refresh > 0) {
            timer = window.setInterval(function(){ 
                nowPlayingInterval();
            }, refresh * 1000);
        }
        
        nowPlayingInterval();
    
        function nowPlayingInterval() {

            // remove error div if exists
            $myDiv.children('.error').remove();

            //create URL
            var url = 'http://ws.audioscrobbler.com/2.0/?callback=?',
                params = {
                    method:  "user.getrecenttracks",
                    format:  "json",
                    limit:   1,
                    user:    options.username,
                    api_key: options.apikey
                };
            
            //sending request
            $.getJSON(url, params, function(data) {
                
                //check for errors
                if ( !data || !data.recenttracks ) {
                    return error('Username "' + options.username + '" does not exist!');
                } else if( !data.recenttracks.track ) {
                    return error('"' + options.username + '" has no tracks to show!');
                }
                
                var track = data.recenttracks.track[0];
                
                if( track && track['@attr'] && track['@attr'].nowplaying == 'true' ) {
                    var html = '';
                    
                    if (options.icon) {
                        html = html + '<img src="' + options.icon + '" class="icon" alt="now playing icon" />';
                    }
                    
                    html = html + '<span class="track">' + track.artist['#text'] + '</span>';
                    html = html + ' - ';
                    html = html + '<span class="track">' + track.name + '</span>';
                    if(track.album['#text']) {
                        html = html + ' (';
                        html = html + '<span class="track">' + track.album['#text'] + '</span>';
                        html = html + ')';
                    }
                    
                    $myDiv.show();
                    update(html);
                } else {
                    if(options.hide) {
                        $myDiv.hide();
                    } else {
                        update(options.notplayingtext)
                    }
                }

            });

        }
        
        function error( message ) {
             $("<p>", {
                    className: "error",
                    html: message
                }).appendTo($myDiv);
                window.clearInterval(timer);
        }
        
        function update( html ) {
            $myDiv.html( html );
        }

    };

    /* ######################## Now Playing Class ends here ################################# */





    
    
    
    /* ##################################### Recent Tracks Function ########################### */
    
    $.fn.lastplayed = function (options) {
        var opts = $.extend({}, $.fn.lastplayed.defaults, options);
        
        if (typeof(options.username) === "undefined") {
            return this;
        }
        
        if (typeof(options.apikey) === "undefined") {
            return this;
        }
        
        return this.each(function(){
            recentTracksClass($(this), opts);
        });
        
    };
    
    $.fn.lastplayed.defaults = {
        limit:          20,
        refresh:        0,
        cover:          true,
        datetime:       true,
        grow:           false,
        shownowplaying: true
    };
    
    
    
    /* ################################# Now Playing Function ################################ */
    
    $.fn.nowplaying = function (options) {
        var opts = $.extend({}, $.fn.nowplaying.defaults, options);
        
        if (typeof(options.username) === "undefined") {
            return this;
        }
        
        if (typeof(options.apikey) === "undefined") {
            return this;
        }
        
        return this.each(function(){
            nowPlayingClass($(this), opts);
        });
        
    };

    $.fn.nowplaying.defaults = {
        refresh:        0,
        icon:           false,
        hide:           false,
        notplayingtext: 'nothing playing'
    };

}(jQuery));
