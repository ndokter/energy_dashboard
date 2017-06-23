<script id="dashboard-template" type="text/template">

    <div class="dashboard">

        <%= test %>

        <div class="widget widget-metric">
            <div class="title">
                <span class="glyphicon glyphicon-flash" aria-hidden="true"></span>
                Electricity
            </div>
            <div class="value">1600 Watt</div>
        </div>
        <div id="graph-electricity-today" class="widget widget-graph"></div>
        <div class="widget widget-metric">
            <table class="table">
                <tr>
                    <td>Electricity</td>
                    <td>3 kWh</td>
                    <td>&euro; 1,43</td>
                </tr>
                <tr>
                    <td>Gas</td>
                    <td>2.5 M<sup>3</sup></td>
                    <td>&euro; 2,86</td>
                </tr>
                <tr>
                    <td colspan="2"></td>
                    <td>&euro; 4,29</td>
                </tr>
            </table>
        </div>
        <div style="clear:both"></div>

        <div class="widget widget-metric">
            <div class="title">
                <span class="glyphicon glyphicon-fire" aria-hidden="true"></span>
                Gas
            </div>
            <div class="value">2.5 M<sup>3</sup></div>
        </div>
        <div id="graph-gas-today" class="widget widget-graph"></div>
        <div style="clear:both"></div>
    </div>
</script>
