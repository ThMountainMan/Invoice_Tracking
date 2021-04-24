<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <!--  This file has been downloaded from bootdey.com    @bootdey on twitter -->
  <!--  All snippets are MIT license http://bootdey.com/license -->
  <title>Invoice</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="http://netdna.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
  <style type="text/css">
    body {
      margin-top: 20px;
      background: #eee;
    }

    .invoice {
      padding: 30px;
    }

    .invoice h2 {
      margin-top: 0px;
      line-height: 0.8em;
    }

    .invoice .small {
      font-weight: 300;
    }

    .invoice hr {
      margin-top: 10px;
      border-color: #ddd;
    }

    .invoice .table tr.line {
      border-bottom: 1px solid #ccc;
    }

    .invoice .table td {
      border: none;
    }

    .invoice .identity {
      margin-top: 10px;
      font-size: 1.1em;
      font-weight: 300;
    }

    .invoice .identity strong {
      font-weight: 600;
    }


    .grid {
      position: relative;
      width: 100%;
      background: #fff;
      color: #666666;
      border-radius: 2px;
      margin-bottom: 25px;
      box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.1);
    }
  </style>


</head>

<body>
  <div class="container">
    <div class="row">
      <!-- BEGIN INVOICE -->
      <div class="col-xs-12">
        <div class="grid invoice">
          <div class="grid-body">
            <div class="invoice-title">
              <div class="row">
                <!-- Insert Logo here
                <div class="col-xs-12">
                  <img src="http://vergo-kertas.herokuapp.com/assets/img/logo.png" alt="" height="35">
                </div>
                -->
              </div>
              <br>
              <div class="row">
                <div class="col-xs-6">
                  <h2>Rechnung - {{invoice.personal.name}}<br>
                    <span class="small"># {{invoice.invoice_id}}</span>
                  </h2>
                </div>
                <div class="col-xs-6 text-right">
                  <h4>
                    <strong>Datum:</strong><br>
                    {{invoice.date}}
                  </h4>
                </div>
              </div>
            </div>
            <hr>
            <br>
            <div class="row">
              <div class="col-xs-6">
                <address>
                  <strong>{{invoice.customer.name}}</strong><br><br>
                  % if invoice.customer.contact:
                  {{invoice.customer.contact}}<br>
                  %end
                  {{invoice.customer.street}}<br>
                  {{invoice.customer.postcode}} {{invoice.customer.city}}<br>
                </address>
              </div>
              <div class="col-xs-6 text-right">
                <h4>Kontakt:</h4>
                {{invoice.personal.name}}<br>
                {{invoice.personal.street}}<br>
                {{invoice.personal.postcode}} {{invoice.personal.city}}<br>
                {{invoice.personal.mail}}<br>
                {{invoice.personal.phone}}<br>
              </div>
            </div>

            <br><br><br>

            <div class="row">
              <div class="col-md-12">
                <h3>SUMMARY</h3>
                <table class="table table-striped">
                  <thead>
                    <tr class="line">
                      <td><strong>Pos.</strong></td>
                      <td class="text-left"><strong>BESCHREIBUNG</strong></td>
                      <td class="text-center"><strong>ANZAHL / STUNDEN</strong></td>
                      <td class="text-center"><strong>PREIS / HONORAR</strong></td>
                      <td class="text-right"><strong>Zwischensumme</strong></td>
                    </tr>
                  </thead>
                  <tbody>
                    % for id, item in enumerate(items):
                    <tr>
                      <td><strong>{{id + 1}}</strong></td>
                      <td>{{item.description}}</td>
                      <td class="text-center">{{item.count}}</td>
                      <td class="text-center">{{"{:.2f}".format(item.cost)}} €</td>
                      <td class="text-right">{{"{:.2f}".format(item.cost * item.count)}} €</td>
                    </tr>
                    % end
                  </tbody>
                </table>

                <table class="table">
                  <tbody>
                    <tr>
                      <td colspan="3"></td>
                      <td class="text-right"><strong>Summe Netto</strong></td>
                      <td class="text-right"><strong>{{"{:.2f}".format(total)}} €</strong></td>
                    </tr>
                    % if invoice.invoice_mwst:
                    <tr>
                      <td colspan="3"></td>
                      <td class="text-right"><strong>zzgl. {{invoice.invoice_mwst}} % MwSt.</strong></td>
                      <td class="text-right"><strong>{{"{:.2f}".format(mwst)}} €</strong></td>
                    </tr>
                    %end
                    <tr>
                      <td colspan="3"></td>
                      <td class="text-right"><strong>Rechnugsbetrag</strong></td>
                      % if invoice.invoice_mwst:
                      <td class="text-right"><strong><big>{{"{:.2f}".format(total_mwst)}} €</big></strong></td>
                      %else:
                      <td class="text-right"><strong><big>{{"{:.2f}".format(total)}} €</big></strong></td>
                      %end
                    </tr>
                  </tbody>
                </table>
                <br>
                <hr>
                <br>
              </div>
            </div>
            <div class="row">
              <div class="text-center">
                <address>
                  <span class="small"> Bitte überweisen Sie den angegebenen Rechnungsbetrag unter Angabe der Rechnungsnummer innerhalb von <b>30 Tagen</b> auf das unten angegebene Konto.<br>
                    <h4>Zahlungsdetails:</h4>
                    <strong>Empfänger:</strong> {{invoice.personal.payment_details.name}} <strong> | </strong>
                    <strong>Bank:</strong> {{invoice.personal.payment_details.bank}} <br>
                    <strong>IBAN:</strong> {{invoice.personal.payment_details.IBAN}} <strong> | </strong>
                    <strong>BIC:</strong> {{invoice.personal.payment_details.BIC}}<br><br>
                    <strong>Steuernummer:</strong> {{invoice.personal.taxnumber}}
                  </span>
                </address>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- END INVOICE -->
    </div>
  </div>
  <script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
  <script src="http://netdna.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
  <script type="text/javascript">

  </script>
</body>

</html>