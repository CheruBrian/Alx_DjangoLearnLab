<form method="POST">
    {% csrf_token %}
    {{ ExampleForm.as_p }}
    <button type="submit">Submit</button>
</form>
