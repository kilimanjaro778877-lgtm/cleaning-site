import os, re, glob

BASE = r"C:\Users\Admin\cleaning-site"

PIXEL_CODE = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1634455044556020');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1634455044556020&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""

# Lead event — fires ONLY on successful form submission
LEAD_EVENT = "if(typeof fbq==='function'){try{fbq('track','Lead');}catch(_){}}"

fixed = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = html

    # 1. Add pixel to <head> if not already there
    if "fbq('init'" not in new and "</head>" in new:
        new = new.replace("</head>", PIXEL_CODE + "\n</head>", 1)

    # 2. Add Lead event after successful form submission
    # Pattern: right after gtag generate_lead event in success handler
    if "generate_lead" in new and "fbq('track','Lead')" not in new:
        new = new.replace(
            "gtag('event', 'generate_lead',",
            LEAD_EVENT + "\n        gtag('event', 'generate_lead',"
        )

    # For pages without gtag but with form success (submitBtn success text)
    if "Заявку прийнято" in new and "fbq('track','Lead')" not in new:
        new = new.replace(
            "submitBtn.textContent = '✅ Заявку прийнято! Передзвонимо.';",
            LEAD_EVENT + "\n        submitBtn.textContent = '✅ Заявку прийнято! Передзвонимо.';"
        )

    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        fixed += 1
        print(f"Added FB pixel: {os.path.basename(path)}")

print(f"\nDone — {fixed} files updated.")
