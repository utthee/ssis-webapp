const toggler = document.querySelector(".toggler-btn");
toggler.addEventListener("click",function(){
    document.querySelector("#sidebar").classList.toggle("collapsed");
})

document.addEventListener("DOMContentLoaded", function () {
  const titleSpan = document.getElementById("page-title");
  const links = document.querySelectorAll(".sidebar-link");

  links.forEach(link => {
    link.addEventListener("click", function (e) {

      links.forEach(l => l.classList.remove("active"));
      this.classList.add("active");
    });
  });
});

document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const registerModal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
    registerModal.hide();

    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();

    document.getElementById('registerForm').reset();
});