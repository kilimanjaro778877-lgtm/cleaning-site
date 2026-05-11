import os, glob

BASE = r"C:\Users\Admin\cleaning-site"

TIKTOK_CODE = """<!-- TikTok Pixel Code Start -->
<script>
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(
var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var r="https://analytics.tiktok.com/i18n/pixel/events.js",o=n&&n.partner;ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=r,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};n=document.createElement("script")
;n.type="text/javascript",n.async=!0,n.src=r+"?sdkid="+e+"&lib="+t;e=document.getElementsByTagName("script")[0];e.parentNode.insertBefore(n,e)};
  ttq.load('D7UFB63C77U471PH8RJG');
  ttq.page();
}(window, document, 'ttq');
</script>
<!-- TikTok Pixel Code End -->"""

# Lead/submit event for TikTok
TTQ_LEAD = "if(typeof ttq!=='undefined'){try{ttq.track('SubmitForm');}catch(_){}}"

fixed = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = html

    # Add TikTok pixel before </body>
    if "D7UFB63C77U471PH8RJG" not in new and "</body>" in new:
        new = new.replace("</body>", TIKTOK_CODE + "\n</body>", 1)

    # Add SubmitForm event alongside existing Lead event
    if "fbq('track','Lead')" in new and "ttq.track('SubmitForm')" not in new:
        new = new.replace(
            "if(typeof fbq==='function'){try{fbq('track','Lead');}catch(_){}}",
            "if(typeof fbq==='function'){try{fbq('track','Lead');}catch(_){}}\n        " + TTQ_LEAD
        )

    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        fixed += 1
        print(f"Added TikTok: {os.path.basename(path)}")

print(f"\nDone — {fixed} files.")
