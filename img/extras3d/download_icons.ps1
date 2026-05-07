$baseDir = "C:\Users\Admin\cleaning-site\img\extras3d"
$logFile = "C:\Users\Admin\cleaning-site\img\extras3d\download_log.txt"

$icons = @(
    @{ name = "vytiazhka"; prompt = "isometric%203D%20icon%20kitchen%20range%20hood%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "shafky"; prompt = "isometric%203D%20icon%20kitchen%20cabinet%20open%20shelves%20clean%20inside%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "mikrokhvylovka"; prompt = "isometric%203D%20icon%20microwave%20oven%20appliance%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "mytia-posudu"; prompt = "isometric%203D%20icon%20stack%20of%20clean%20dishes%20plates%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "dushova"; prompt = "isometric%203D%20icon%20shower%20cabin%20glass%20door%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "plytka"; prompt = "isometric%203D%20icon%20bathroom%20tile%20wall%20cleaning%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "balkon"; prompt = "isometric%203D%20icon%20balcony%20terrace%20clean%20floor%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "svitylnyky"; prompt = "isometric%203D%20icon%20ceiling%20pendant%20lamp%20light%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "garderobna"; prompt = "isometric%203D%20icon%20wardrobe%20closet%20with%20clothes%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" },
    @{ name = "orhanizatsiia"; prompt = "isometric%203D%20icon%20storage%20bins%20organized%20shelves%20pastel%20blue%20white%20soft%20shadows%20white%20background%20cute%20minimal%20product%20render%20no%20text" }
)

Add-Content $logFile ("START: " + (Get-Date))

foreach ($icon in $icons) {
    $outPath = $baseDir + "\" + $icon.name + ".jpg"
    if ((Test-Path $outPath) -and (Get-Item $outPath).Length -gt 5000) {
        Add-Content $logFile ("SKIP: " + $icon.name + " already exists")
        continue
    }
    $url = "https://image.pollinations.ai/prompt/" + $icon.prompt + "?width=256&height=256&nologo=true&seed=42&model=flux"
    
    $ok = $false
    for ($attempt = 1; $attempt -le 5; $attempt++) {
        Start-Sleep -Seconds 20
        try {
            $headers = @{ "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" }
            Invoke-WebRequest -Uri $url -OutFile $outPath -TimeoutSec 90 -Headers $headers
            $size = (Get-Item $outPath).Length
            if ($size -gt 5000) {
                Add-Content $logFile ("OK: " + $icon.name + " = " + $size + " bytes")
                $ok = $true
                break
            } else {
                Add-Content $logFile ("SMALL: " + $icon.name + " = " + $size + " bytes, retry " + $attempt)
            }
        } catch {
            Add-Content $logFile ("ERR: " + $icon.name + " attempt " + $attempt + ": " + $_)
        }
    }
    if (-not $ok) {
        Add-Content $logFile ("FAILED: " + $icon.name)
    }
}

Add-Content $logFile ("DONE: " + (Get-Date))
