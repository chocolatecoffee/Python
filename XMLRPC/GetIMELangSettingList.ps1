$Langs = (Get-WinUserLanguageList).LocalizedName

foreach($_ in $Langs){

    switch($_){
        "Japanese" {Write-Output "日本語"}
        "English (United States)" {Write-Output "英語"}
        "Dutch (Netherlands)" {Write-Output "オランダ語"}
        "Italian (Italy)" {Write-Output "イタリア語"}
        "Spanish (Spain)" {Write-Output "スペイン語 (スペイン)"}
        "German (Germany)" {Write-Output "ドイツ語 (ドイツ)"}
        "French (Canada)" {Write-Output "フランス語 (カナダ)"}
        "French (France)" {Write-Output "フランス語 (フランス)"}
        "Portuguese (Portugal)" {Write-Output "ポルトガル語"}
        "Russian" {Write-Output "ロシア語"}
        "Korean" {Write-Output "韓国語"}
        "Chinese (Simplified, China)" {Write-Output "中国語 (中国)"}
        "Chinese (Traditional, Taiwan)" {Write-Output "中国語 (台湾"}
        "Chinese ??" {Write-Output "中国語 (GoogleIME)"}

        default {Write-Output $_}
    }
}