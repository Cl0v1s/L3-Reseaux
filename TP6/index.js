var Menu = {
    state : null,
    target : null,

    init : function(e)
    {
        this.target = document.querySelector(e);
        this.close();
        let self = this;
        this.target.parentElement.addEventListener("mouseover", function()
        {
            self.open();
        });
        this.target.parentElement.addEventListener("mouseout", function()
        {
            self.close();
        });
    }, 

    switch : function()
    {
        if(this.state == 0)
            this.open();
        else 
            this.close();
    },

    close: function()
    {
        this.state = 0;
        this.target.style.height = "0";
    }, 

    open : function()
    {
        this.state = 1;
        this.target.style.height = "initial";
    }
}



function Main()
{
    Menu.init("header nav");
}

window.onload = Main;