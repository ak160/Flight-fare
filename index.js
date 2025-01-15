function navigation(){
    document.addEventListener("DOMContentLoaded", () => {
        const menuIcon = document.querySelector(".menu-icon");
        const dropdownMenu = document.querySelector(".dropdown-menu");
      
        // Toggle dropdown menu visibility
        menuIcon.addEventListener("click", () => {
          const isMenuVisible = dropdownMenu.style.display === "block";
          dropdownMenu.style.display = isMenuVisible ? "none" : "block";
        });
      
        // Close dropdown when clicking outside
        document.addEventListener("click", (e) => {
          if (!menuIcon.contains(e.target) && !dropdownMenu.contains(e.target)) {
            dropdownMenu.style.display = "none";
          }
        });
      });
      
}
navigation();