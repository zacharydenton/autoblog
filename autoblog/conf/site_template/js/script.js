(function($) {
	$(function() {
    	$('.answer_toggle').click(function() {
        	$(this).prev('.answer').slideToggle();
    	});
        $("#github-projects").loadRepositories("zacharydenton");
        $("#euler-commits").latestCommits('zacharydenton', 'euler', 5);
        $('#latest-music').lastplayed({
            apikey:     'b25b959554ed76058ac220b7b2e0a026',
            username:   'zacharydenton',
            limit:      5,
            refresh:    30
        });
	});
})(jQuery);
