try{
    cd $args[0]
    Invoke-Expression $args[1]
    exit 0
} 
catch [System.Management.Automation.CommandNotFoundException]{
    exit 1
}
