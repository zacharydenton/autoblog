# Adopted from Scott Kyle's Rakefile
# http://github.com/appden/appden.github.com/blob/master/Rakefile

task :default => :server

desc 'Build site with Jekyll'
task :build do
	jekyll
end

desc 'Build and start server with --auto'
task :server do
	jekyll '--server --auto'
end

desc 'Build and deploy'
task :deploy => :build do
	sh 'rsync -rtzh --progress --delete site/_site/ zacharydenton@zacharydenton.com:~/zacharydenton.com/'
end

def jekyll(opts = '')
    sh 'python autoblog.py'
	sh 'rm -rf site/_site'
	sh 'cd site; jekyll ' + opts
end


