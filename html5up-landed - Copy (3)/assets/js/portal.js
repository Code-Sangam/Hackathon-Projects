(function(){
	function el(tag, cls){ var e = document.createElement(tag); if(cls) e.className = cls; return e; }
	function card(title, meta){ var b = el('div','box'); b.innerHTML = '<strong>'+title+'</strong><br/><span>'+meta+'</span>'; return b; }
	function range(n){ return Array.from({length:n}, (_,i)=>i); }
	function sample(list){ return list[Math.floor(Math.random()*list.length)]; }

	var alumniNames = ['Aarav Mehta','Isha Kapoor','Rohan Gupta','Meera Nair','Dev Patel','Ananya Rao'];
	var studentNames = ['Nikhil Sharma','Priya Singh','Karan Das','Sneha Roy','Arjun Iyer','Ritu Jain'];
	var roles = ['Software Engineer','Data Scientist','Product Manager','Hardware Engineer','Web Developer'];
	var depts = ['CSE','ECE','ME','IT','AI/ML'];
	var locations = ['Bengaluru','Delhi','Mumbai','Pune','Hyderabad'];

	document.addEventListener('DOMContentLoaded', function(){
		// Chat
		var chatList = document.getElementById('common-chat-list');
		var chatInput = document.getElementById('common-chat-input');
		var chatSend = document.getElementById('common-chat-send');
		if(chatList && chatSend){
			chatSend.addEventListener('click', function(){
				var t = (chatInput.value||'').trim();
				if(!t) return;
				var b = el('div','box');
				b.textContent = t;
				b.style.marginBottom = '0.5rem';
				chatList.prepend(b);
				chatInput.value = '';
			});
		}

		// Alumni list
		var alumniCards = document.getElementById('alumni-cards');
		if(alumniCards){ range(12).forEach(function(){ alumniCards.appendChild(card(sample(alumniNames), sample(roles)+' · '+sample(locations))); }); }

		// Student list
		var studentCards = document.getElementById('student-cards');
		if(studentCards){ range(12).forEach(function(){ studentCards.appendChild(card(sample(studentNames), sample(depts)+' · '+sample(locations))); }); }

		// Projects
		var projectCards = document.getElementById('project-cards');
		var projectPost = document.getElementById('project-post');
		if(projectCards){ range(8).forEach(function(){ projectCards.appendChild(card('Project '+(Math.random()*100|0), 'By '+sample(alumniNames.concat(studentNames)))); }); }
		if(projectPost){ projectPost.addEventListener('click', function(){
			var title = (document.getElementById('project-title').value||'').trim();
			if(!title) return;
			projectCards.prepend(card(title, 'By You'));
			document.getElementById('project-form').reset();
		}); }

		// Profiles (alumni/student)
		try{
			var step = sessionStorage.getItem('signupStep1');
			if(step){
				var s = JSON.parse(step);
				if(document.getElementById('ap-name')){
					document.getElementById('ap-name').textContent = s.fullName || '-';
					document.getElementById('ap-role').textContent = s.currentRole || '-';
					document.getElementById('ap-college').textContent = s.collegeName || '-';
					document.getElementById('ap-location').textContent = sample(locations);
					setCounts('ap-followers','ap-following','ap-projects');
					populate('ap-project-list', 6);
				}
				if(document.getElementById('sp-name')){
					document.getElementById('sp-name').textContent = s.fullName || '-';
					document.getElementById('sp-dept').textContent = s.department || '-';
					document.getElementById('sp-college').textContent = s.collegeName || '-';
					document.getElementById('sp-location').textContent = sample(locations);
					setCounts('sp-followers','sp-following','sp-projects');
					populate('sp-project-list', 6);
				}
			}
		}catch(e){}
	});

	function setCounts(followersId, followingId, projectsId){
		var followers = (50 + Math.random()*450) | 0;
		var following = (20 + Math.random()*280) | 0;
		var projects = (5 + Math.random()*20) | 0;
		var fEl = document.getElementById(followersId);
		var foEl = document.getElementById(followingId);
		var pEl = document.getElementById(projectsId);
		if(fEl) fEl.textContent = followers;
		if(foEl) foEl.textContent = following;
		if(pEl) pEl.textContent = projects;
	}

	function populate(containerId, n){
		var elc = document.getElementById(containerId); if(!elc) return;
		for(var i=0;i<n;i++){ elc.appendChild(card('Project '+(Math.random()*100|0),'Demo')); }
	}
})();
