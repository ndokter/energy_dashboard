<script id="report-graph-wrapper-template" type="text/template">
    <div class="energy-graph-wrapper panel panel-primary">
        <div class="panel-heading">
            <div class="btn-group date-period" role="group">
              <button type="button" data-period='hours' class="btn btn-default active">Uren</button>
              <button type="button" data-period='days' class="btn btn-default">Dagen</button>
              <button type="button" data-period='months' class="btn btn-default">Maanden</button>
            </div>

            <div class="btn-group" role="group">
                <button type="button" class="btn btn-default btn-sm previous-date">
                    <span class="glyphicon glyphicon-menu-left" aria-hidden="true"></span>
                </button>
                <button type="button" class="btn btn-default btn-sm next-date">
                    <span class="glyphicon glyphicon-menu-right" aria-hidden="true"></span>
                </button>
            </div>

            <span class="current-date"></span>

            <div class="btn-group data-type" role="group">
                <button type="button" data-type="usage" class="btn btn-default">Verbruik</button>
              <button type="button" data-type="costs" class="btn btn-default active">Kosten</button>
            </div>
        </div>
        <div class="panel-body"></div>
    </div>
</script>
<script id="actual-graph-wrapper-template" type="text/template">
    <div class="energy-graph-wrapper panel panel-primary">
        <div class="panel-body"></div>
    </div>
</script>
