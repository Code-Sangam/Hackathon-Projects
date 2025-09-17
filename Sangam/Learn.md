## Deploy Option B: Frontend on AeonFree, Backend on Render (MongoDB Atlas)

This is a fully click-by-click guide. You’ll do it in this order:
- Create MongoDB Atlas database (free)
- Deploy Node/Express backend on Render
- Upload frontend to AeonFree and point it to the backend
- Verify end-to-end and fix common issues

---

### Part 1 — Create MongoDB Atlas database (free, click-by-click)

1) Sign up and log in
- Open your browser and go to ` `.
- Click “Try Free” or “Start Free” → sign up (Google or email) → verify your email if prompted.
- After login, you will land in Atlas UI.

2) Create a new project (if Atlas asks)
- If you see a prompt “Create a Project”: enter Project Name: `Sangam` → click “Next” or “Create Project”.
- Invite Members step: click “Create Project” (you can skip adding members).

3) Create a free cluster
- You should be on the Project Home. Click the big button “Build a Database”.
- Choose “Starter Plan (Shared) · Free M0”. Click “Create”.
- Choose a Cloud Provider/Region. Example: “AWS” and “N. Virginia (us-east-1)”. Pick one near Render region.
- Keep all defaults (Cluster Tier = M0, additional settings default).
- Click “Create Deployment”. This will take 1–3 minutes to provision.

4) Create a database user
- While cluster is creating, a side panel may appear: “Create a Database User”.
- Username: `sangam_user` (or any). Password: click “Autogenerate Secure Password” or set your own; copy/save it.
- Select “Read and write to any database”. Click “Create Database User”.

5) Allow network access (IP Access List)
- In the same panel, click “Add IP Address”. Choose “Allow Access From Anywhere”. This adds `0.0.0.0/0`.
- Click “Add Entry”. You can lock this down later.

6) Get your connection string (URI)
- Once the cluster is “Ready”, click “Connect”.
- Choose “Drivers”.
- Copy the “Connection string for your application”. It looks like:
  `mongodb+srv://sangam_user:<PASSWORD>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority&appName=<cluster-name>`
- Modify it to include a database name (optional but clearer):
  `mongodb+srv://sangam_user:<PASSWORD>@<cluster-name>.mongodb.net/alumni_platform?retryWrites=true&w=majority`
- Replace `<PASSWORD>` with your saved password. Save the full URI; you’ll paste it into Render.

---

### Part 2 — Deploy the backend to Render (click-by-click)

What you’re deploying: this repo’s `server.js` as a web service. It must read `process.env.PORT` (already done) and `MONGO_URI`.

1) Prepare your repo online
- Push this project to a GitHub repository (if not already). From your machine: create a repo, commit, and push.
- Minimum files needed: `server.js`, `package.json`, `package-lock.json`.

2) Create a Render account and service
- Go to `https://render.com/` → “Sign Up” (GitHub/Google/email) → log in.
- In the Render Dashboard, click the “New +” button (top-right).
- Click “Web Service”.

3) Connect your repository
- “Connect a repository”: click “Connect” next to your GitHub, authorize if asked.
- Find your repo in the list and click it. Or choose “Public Git repository” and paste the URL.

4) Configure the service
- Name: `sangam-backend` (anything).
- Region: choose near your MongoDB region (e.g., Ohio/US East).
- Branch: `main` (or your default branch).
- Runtime: Auto-detected Node. Ensure Node version ≥ 18 (Render usually handles it).
- Build Command: leave blank.
- Start Command: `node server.js`.

5) Add environment variables
- Scroll to “Environment Variables” → click “Add Environment Variable”.
- Key: `MONGO_URI` → Value: paste the Atlas URI from Part 1.
- Click “Save”.

6) Create and deploy
- Click “Create Web Service”. Render starts building and deploying.
- Wait for Status: “Live”. Click into the service to view details.

7) Confirm logs
- Click the “Logs” tab. Look for a line similar to: `MongoDB connected` and `Server running on http://localhost:<port>`.
- If you see Mongo errors, recheck your `MONGO_URI` and Atlas IP Allow List.

8) Get the public URL
- On the service “Overview” tab, copy the URL at the top, e.g., `https://sangam-backend.onrender.com`.
- You’ll paste this into the frontend config in Part 3.

Optional: quick API test
- On your computer, open Terminal/PowerShell and run:
  `curl -X POST "https://<your-render-subdomain>.onrender.com/api/login" -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\"}"`
- Expected: a JSON response (likely `User not found` until you sign up via UI).

---

### Part 3 — Upload frontend to AeonFree and point it to backend (click-by-click)

Your frontend is pure HTML/CSS/JS. It’s already wired to read a global `window.API_BASE` from `assets/js/config.js` and call the backend.

1) Create AeonFree account
- Go to `https://aeonfree.com/` → click “Sign Up” → complete registration → verify email.
- After login, click “Create New Account” or “+ Create New”.

2) Create a hosting account
- Domain selection page:
  - To use their free subdomain: choose “Select our Subdomain”, enter a subdomain (e.g., `sangam-demo`) and select an available ending (e.g., `.hstn.me`). Click “Check subdomain” → if available, proceed.
  - To use your own domain: choose “Add your own Domain”. Set your domain’s nameservers at your registrar to:
    - `ns1.hstn.me`
    - `ns2.hstn.me`
    Then return and enter your domain; click “Check Domain Name”.
- Set a strong password (used for control panel/FTP). Click “Create Hosting Account”.
- Wait 2–5 minutes for status to become “Active”. You’ll also receive an email with details.

3) Open File Manager and go to `htdocs`
- From your AeonFree dashboard, click the hosting account → click “Control Panel”.
- In the control panel, click “File Manager”.
- In the left tree or main pane, double-click the folder `htdocs/` (this is the web root).

4) Upload your site files
- Click the “Upload” button.
- Select and upload the contents of your local project folder except the following (do NOT upload these):
  - `node_modules/`
  - `server.js`
  - `auth.sqlite`
  - `package.json` and `package-lock.json`
- After upload, confirm:
  - `htdocs/index.html` exists
  - `htdocs/assets/...` and `htdocs/images/...` folders are present

5) Set the backend URL in config.js
- In File Manager, navigate to `htdocs/assets/js/`.
- Click `config.js` → click “Edit”.
- Set the line to your Render URL (no trailing slash):
  `window.API_BASE = 'https://<your-render-subdomain>.onrender.com';`
- Click “Save” (or the Save icon), then “Close Editor”.

6) Issue SSL (HTTPS)
- In the Control Panel, look for “SSL/TLS” or “Security” section.
- Click “Install SSL” or “Issue SSL Certificate” for your domain/subdomain.
- Follow prompts; wait until status shows the certificate is active.
- Always access your site via `https://your-subdomain.hstn.me` (or your domain).

7) Test that pages load
- Open your site URL in a new browser tab.
- Press F12 → open “Console” and “Network” tabs. Reload the page.
- Ensure no 404s for CSS/JS files. If you see 404s, re-check your uploaded folder structure.

---

### Part 4 — Verify end-to-end (click-by-click)

1) Student signup flow
- Go to `https://<your-frontend-domain>/index.html` → click “Student Sign Up”.
- Fill the form (Step 2) → click “Continue” (goes to Set Password page).
- On Set Password page, enter email or mobile + password/confirm → click “Finish Signup”.
- In DevTools → Network, you should see a POST to:
  `https://<your-render-subdomain>.onrender.com/api/signup/student`
- Expected Response: `{ "success": true, "message": "Student signup stored" }`.
- You should be redirected to the student/alumni profile page based on role.

2) Alumni signup flow
- Similarly, do “Alumni Sign Up” → fill → “Continue” → “Finish Signup”.
- Check the Network request to `/api/signup/alumni` returns success.

3) Login flow
- Visit `login.html` → enter previously used email/mobile + any password (demo accepts if user exists) → click “Login”.
- Network should show POST `/api/login` → Response `{ success: true, message: 'Login success', user: ... }` → you’re redirected.

4) General UI
- Visit `projects.html`, `chat.html`, `student-profile.html`, `alumni-profile.html` to ensure assets load.

---

### Common problems and exact fixes

- API calls failing with 404 on AeonFree
  - Cause: Frontend is calling `/api/...` locally instead of your backend.
  - Fix: In `htdocs/assets/js/config.js` set:
    `window.API_BASE = 'https://<your-render-subdomain>.onrender.com';`
    Make sure `config.js` loads before `auth.js`. It already does in `login.html`, `student-signup.html`, `alumni-signup.html`, `set-password.html`.

- CORS error (Blocked by CORS policy)
  - Cause: Backend CORS misconfiguration (later tightened).
  - Fix: In `server.js`, we use `app.use(cors())` which allows all origins. If you restrict CORS, add your AeonFree domain to the allowed origins list.

- Mixed content blocked
  - Cause: Frontend served over HTTPS but backend URL is `http://`.
  - Fix: Always use `https://` in `window.API_BASE`.

- MongoDB connection failed / timeout
  - Check Render → Service → Logs. If you see authentication/timeout errors:
    - Verify `MONGO_URI` is correct (username/password exact, includes db name).
    - In Atlas → Network Access, ensure IP Access List includes `0.0.0.0/0` (quick start) or the proper egress IPs.

- `sqlite3` install/build fails on Render
  - This project primarily uses MongoDB. If Render build fails on `sqlite3`, remove it:
    - Delete `sqlite3` from `package.json` dependencies.
    - Remove the SQLite code blocks in `server.js` (open, create table, insert). The app will still work with MongoDB.
    - Commit and redeploy.

- Backend port errors
  - Ensure `server.js` uses `process.env.PORT` (it does). Don’t hardcode a port on Render.

---

### Optional — Use your own domain on AeonFree (click-by-click)

1) At your domain registrar
- Set the nameservers to:
  - `ns1.hstn.me`
  - `ns2.hstn.me`
- Save and wait for DNS propagation (may take up to a few hours).

2) In AeonFree Control Panel
- Add your domain to the hosting account if not already.
- Issue a free SSL certificate for the domain.
- Access your site using `https://yourdomain.com`.

---

### Quick reference (what to paste where)

- Render → Web Service → Environment Variables:
  - `MONGO_URI = mongodb+srv://sangam_user:<PASSWORD>@<cluster>.mongodb.net/alumni_platform?retryWrites=true&w=majority`

- AeonFree → File Manager → `htdocs/assets/js/config.js`:
  - `window.API_BASE = 'https://<your-render-subdomain>.onrender.com';`

---

### Final checklist before announcing “Done”

- You can open the frontend via HTTPS and no asset 404s appear.
- Signup (student and alumni) return `{ success: true }` in Network.
- Login returns `{ success: true }` and redirects.
- Render logs show “MongoDB connected” and API requests during your actions.

You’re done: frontend on AeonFree, backend on Render, database on Atlas.


