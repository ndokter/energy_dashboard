import React from 'react';
import jQuery from 'jquery';
import FlotChart from './flotChart';
import ReactBootstrap from 'react-bootstrap';

// React-Bootstrap mappings
var Checkbox = ReactBootstrap.Checkbox,
    Col = ReactBootstrap.Col,
    FormGroup = ReactBootstrap.FormGroup,
    Label = ReactBootstrap.Label,
    Row = ReactBootstrap.Row,
    $ = jQuery;

var BaseBox = React.createClass({
    getInitialState: function() {
        return {data: []};
    },
    fetchData: function(power_meter, interval, start, end) {
        start.setMilliseconds(0);
        end.setMilliseconds(0);
        $.ajax({
            url: '/api/reading-report/'+power_meter+'/'+interval+'/'+start.toISOString()+'/'+end.toISOString()+'/',
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    componentDidMount: function() {
        var last_year = new Date();
            last_year.setFullYear(2015)
        this.fetchData(1, 'hourly', last_year, new Date())
    },
    render: function() {
        var series = [];
        this.state.data.map(function(reading){
            series.push([new Date(reading.datetime), parseFloat(reading.value_increment)]);
        });
        var plotData = [
            {
                data: series,
                color: 'rgb(86, 175, 232)',
                shadowSize: 0,
                label: 'Meter #1',
                stack: true,
                lines: {
                    lineWidth: 2,
                    show: true,
                    fill: true
                }
            },
        ]
        return (
            <FlotChart style={{height: 250}} plotData={plotData} />
        );
    }
});


var Page = React.createClass({
    render: function() {
        return (
            <Row>
                <Col xs={12} md={8}>
                    <PowerMeterWrapper />
                    <BaseBox />
                </Col>
            </Row>
        );
    }
});

export default Page;