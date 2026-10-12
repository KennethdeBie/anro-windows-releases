import os,sys,json,urllib.request,urllib.error,urllib.parse,subprocess,re
SOURCE='KennethdeBie/anro-juweliers-metadata-importer'
DEST='KennethdeBie/anro-windows-releases'
run,version=sys.argv[1:]
if not run.isdigit() or not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)',version): raise SystemExit('Invalid run/version')
# Use the configured GitHub CLI credential only for normal GitHub API calls.
# Never log it, store it in the release, or transfer it to the publisher workflow.
token=subprocess.check_output(['gh','auth','token'],text=True).strip()
headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json'}
def api(path):
 with urllib.request.urlopen(urllib.request.Request('https://api.github.com/'+path,headers=headers),timeout=30) as response: return json.load(response)
status=api(f'repos/{SOURCE}/actions/runs/{run}')
if status['status']!='completed' or status['conclusion']!='success': raise SystemExit('The Windows build must be successful before publication')
artifacts=api(f'repos/{SOURCE}/actions/runs/{run}/artifacts')['artifacts']
artifact=next((a for a in artifacts if a['name']=='anro-windows-x64-installer' and not a['expired']),None)
if not artifact: raise SystemExit('No verified installer artifact')
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl): return None
try: urllib.request.build_opener(NoRedirect()).open(urllib.request.Request(artifact['archive_download_url'],headers=headers),timeout=30)
except urllib.error.HTTPError as error:
 if error.code!=302: raise
 location=error.headers.get('Location','')
else: raise SystemExit('Missing temporary download redirect')
parsed=urllib.parse.urlparse(location)
if parsed.scheme!='https' or not re.fullmatch(r'productionresultssa[0-9]+\.blob\.core\.windows\.net',parsed.hostname or ''): raise SystemExit('Unexpected GitHub artifact download host')
# This short-lived read-only URL grants access only to the selected distribution ZIP.
# All files in that ZIP are explicitly intended for public release; CI validates them again.
payload=json.dumps({'ref':'main','inputs':{'artifact_url':location,'version':version,'source_run':run}})
result=subprocess.run(['gh','api','--method','POST',f'repos/{DEST}/actions/workflows/publish-windows.yml/dispatches','--input','-'],input=payload,text=True,capture_output=True)
if result.returncode: raise SystemExit('GitHub release dispatch failed: '+result.stderr)
print('Dispatched verified release '+version+' from successful Windows build '+run)
