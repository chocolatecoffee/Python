# Get-AppPackage | Sort-Object Name | Select-Object Name

$Res_App = Get-AppxPackage | Select-Object Name

foreach($_ in $Res_App){
    $AppName = $_ | Select-Object Name 

    switch($AppName.Name.ToString()){

        "Microsoft.Windows.Photos" {Write-Output "フォト"}
        "Microsoft.WindowsCamera" {Write-Output "カメラ"}
        "Microsoft.SkypeApp" {Write-Output "Skype"}
        "Microsoft.WindowsCalculator" {Write-Output "電卓"}
                
        default {}
    }

}