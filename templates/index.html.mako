<%
    some_element = my_list[3]
%>
<html>
    <head>
        <title>Order details</title>
    </head>
    <body>


        <%
            some_element = my_list[3]
        %>

    <div class="container">
        <p>My string: ${my_string}</p>
        <p>Value from the list: ${some_element}</p>
        <p>Loop through the list:</p>
        <ul>
            % for n in my_list:
                <li>${n}</li>
            % endfor
        </ul>
    </div>


    </body>
</html>