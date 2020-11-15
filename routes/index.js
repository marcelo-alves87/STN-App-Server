var express = require('express');
var multer = require('multer');
var fs = require('fs');
var router = express.Router();
var path = require("path");
var exec = require("child_process").exec;
const UPLOAD_PATH = '../python/';
var uuid = require('uuid')



router.post('/checkConnectionAndCalibrationStatus', function(req,res){
    /*
    0 - Sem conexao, 1 - Sem calibracao, 2 - Calibracao encontrada, e retornar a data da calibracao
    */
    
   checkConnection(res);

   
   /*  if(data1 == 0) {
        res.json({'status' : 0});
    } else {
        data1 = setTimeout(checkCalibrationStatus, timeout1);
        console.log(data1);
    } */ 

  

    
    
});

function checkConnection(res) {


    exec('python3 /home/pi/Documents/STN_Server/python/CheckConnection.py', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {
            
          //console.log(stdout)
          if(stdout.trim() === 'erro') {
            res.json({'status' : 0})
          } else {
            res.json({'status' : 1})  
            //checkCalAlreadySaved(res);
           }
        }
    });
}

router.post('/checkCalAlreadySaved', function(req, res) {
     exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py "0.1"', (error, stdout, stderr) => {
            if (error) {
              console.error(error);
            } 
            else if(stderr) {
              console.log(stderr)  
            }
            else {          
              if(stdout.trim() === '0.1.0') {
                res.json({'status' : 0});
              } else {       
                console.log(stdout)  
                res.json({'status' : 1, 'date' : stdout});
              }
            }
    });
});


router.post('/startNewCalibration', function(req, res) {
    startNewCalibration(res);
});

function startNewCalibration(res) {
    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 0', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {     
          console.log(stdout);      
          if(stdout.trim() === 'erro') {
            res.json({'status' : '1.0'});
          } else {  
            res.json({'status' : '1.1'});
          }
        }
    });
}

router.post('/openCalibrationStatus', function(req,res){
    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 1', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {           
          console.log(stdout);  
          if(stdout.trim() === 'erro') {
            res.json({'status' : '2.0'});
          } else {  
            res.json({'status' : '2.1'});
          }
        }
    });
});

router.post('/shortCalibrationStatus', function(req,res){
    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 2', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {           
            console.log(stdout);
            if(stdout.trim() === 'erro') {
            res.json({'status' : '3.0'});
          } else {  
            res.json({'status' : '3.1'});
          }
        }
    });
});

router.post('/loadCalibrationStatus', function(req,res){
    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 3', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {           
          console.log(stdout);  
          if(stdout.trim() === 'erro') {
            res.json({'status' : '4.0'});
          } else {  
            res.json({'status' : '4.1'});
          }
        }
    });
});


router.post('/saveCalibrationStatus', function(req,res){
    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 4', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {           
          console.log(stdout);  
          if(stdout.trim() === 'erro') {
            res.json({'status' : '5.0'});
          } else {  
            res.json({'status' : '5.1'});
          }
        }
    });
});

router.post('/fileProcess', function(req,res) {
    execPython_RNN(res);
    //   processEncodedFile(JSON.stringify(req.body.fileName), res, req.body.typeProcess);
    
        // 1 - Checar conexao com o instrumento
    
        // 2 - Calibrar o instrumento de forma eletronica, dado o arquivo de calibracao
    
        // 3 - Pegar o arquivo do instrumento e salva lo com Pi.csv
    
        // 4 - Usar Convert to Model para gerar a entrada da rede neural
       
      //  data = JSON.stringify(req.body);
        
      //  data = JSON.parse(data);
        
       // console.log(data);
      //  extractDataFromVNA(data, res);
        /*if(data != undefined && data[0] != undefined) {
            //operador = data[0]['operador'];
            //linha = data[1]['linha'];
            //torre = data[2]['torre'];
            //estai = data[3]['estai'];
        
        
            extractDataFromVNA(data, res);
        
       } else {
            res.json({'data' : 0});
       }*/
       
       // setTimeout(execPython_Conversion, 1000, res);
        
    
        // 5 - Executar a rede como parametro o model da etapa anterior
        
    
        // 6 - gerar o relatorio
    
    
       //res.json({'print' : 1 });
    });


function extractDataFromVNA(data, res) {

    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 5', (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
            if(stdout.trim()==='5.0') {
                res.json({'data' : 0});
            } else {
                convertDataToXlsx(res);
            }           
        }
    });

}

function convertDataToXlsx(res) {

    exec('python3 /home/pi/Documents/STN_Server/python/ConvertToModel.py', (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
            if(stdout.trim() === 'erro') {
                res.json({'data' : 0});
            } else {
                //execPython_RNN(res);

            }
        }
    });

}

function execPython_RNN(res) {
  
    exec('python3 /home/pi/Documents/STN_Server/python/Workshop.py', (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
            if(stdout) {
                getMeanMode(stdout, res)
                
            } else if (stderr) {
                console.log(stderr)
                res.json({'data' : 0});

            }
            
        }
    });
}

function getMeanMode(input1, res) {
    exec('python3 /home/pi/Documents/STN_Server/python/GetMeanMode.py ' + input1, (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
            if(stdout) {
                res.json({'data' : stdout});
            } else if (stderr) {
                console.log(stderr)
                res.json({'data' : 0});

            }
            
        }
    });
}

router.post('/shutdown', function(req, res) {

    exec('python3 /home/pi/Documents/STN_Server/python/Shutdown.py', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } else if(stderr) {
            console.log(stderr);
        }
    });

});

router.post('/startMeasurement', function(req, res) {

    data = JSON.stringify(req.body);
        
    data = JSON.parse(data);
    
    if(data != undefined && data.corr != undefined) {
        extractDataFromVNA_Corr(data, res);
    
    }
    /*if(data != undefined && data[0] != undefined) {
        
    
        /*operador = data[0]['operador'];
        linha = data[1]['linha'];
        torre = data[2]['torre'];
        estai = data[3]['estai'];
        corr = data[data.length - 1]['corr'];   
        
        console.log(corr)    
        //extractDataFromVNA(data, res);
 
    } */
    
    
    
});

function extractDataFromVNA_Corr(input_argv, res) {

    exec('python3 /home/pi/Documents/STN_Server/python/CheckCalibrationStatus.py 6 ' + input_argv.corr, (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:');
          console.error(error);
        } else if (stderr) {
           res.json({'data' : -1}); 
        } else {
            console.log(stdout)
            if(stdout.trim()==='erro') {
               console.log('erro1')
               res.json({'data' : -1});
            } else if(stdout.trim()==='0') {
               //corr necessita de mais medicoes  
               res.json({'data' : 0}) ; 
            } else if(stdout.trim==='semCorrelacao') {
               //medicoes sem corr  
               res.json({'data' : 1}) ;
            } else {
               corr = parseFloat(stdout)
               if(corr == 1) {
                    // corr sucesso
                    res.json({'data' : 2});
               } else {
                    res.json({'data' : 3, 'corr' : corr});
               }
                        
            }          
        }
    });

}


            
/* var store = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, './python');
    },
    filename: function(req, file, cb) {
        cb(null, file.originalname);
    }
});

router.get('/', function(req,res) {
    res.json('Hello World!');
});

var upload = multer({storage: store}).single('file');

router.post('/fileUpload', function (req, res, next) {
    upload(req, res, function(err) {
        if(err) {
            return res.status(501).json({error:err});
        }

        return res.json({originalname:req.file.originalname, uploadname: req.file.filename})
    });
}); */


/* function unlinkSyncFile(fileName) {
    path1 = path.resolve(__dirname, UPLOAD_PATH, fileName);
    if(fs.existsSync(path1)) {
        fs.unlinkSync(path1);
    }
}

function execPython(fileName, res, basename) {
    //STN - MED02mWorkshop - R.04.2019 - RNA.1001.14.1
    //STN - MEDExpUFPEWorkshop - R.03.2019 - RNA.1001.14.1
    exec('python ./python/' + '"' + basename + '.py" ' + '"' + fileName + '"', (error, stdout, stderr) => {
        if (error) {
          console.error('exec error:' + error);
          return;
        }
        res.json({'print' : stdout });            
        setTimeout(unlinkSyncFile, 1000, fileName);
    });
}

function execPython2(fileName, res) {
    exec('python ./python/plot.py ' + '"' + fileName + '"', (error, stdout, stderr) => {
        if (error) {
          console.error('exec error:' + error);
          return;
        }
       
        res.json({'image' : base64_encode(fileName + '.png')});
       
        setTimeout(unlinkSyncFile, 1000, fileName);    
        setTimeout(unlinkSyncFile, 2000, fileName + '.png');
     
      });
} */

/* function processEncodedFile(fileEncoded, res, typeProcess) {
    fileEncoded = fileEncoded.replace('data:application/vnd.ms-excel;base64,', '');
    fileEncoded = fileEncoded.replace('data:text/comma-separated-values;base64,', '');
    fileName = uuid.v4().toString() + '.csv';
    fs.writeFile('python/' + fileName, fileEncoded, 'base64', function(err) {
        if(err) {
            console.log(err);
        } else {
            if(typeProcess == 0) {
                setTimeout(execPython, 1000, fileName, res, 'STN - MED02mWorkshop - R.04.2019 - RNA.1001.14.1');
            } else if (typeProcess == 1) {
                setTimeout(execPython, 1000, fileName, res, 'STN - MEDExpUFPEWorkshop - R.03.2019 - RNA.1001.14.1');
            } else if(typeProcess == 2) {
                setTimeout(execPython2, 1000, fileName, res);
            }
        }
    });
} */

/* // function to encode file data to base64 encoded string
function base64_encode(fileName) {
    path1 = path.resolve(__dirname, UPLOAD_PATH, fileName);
    if(fs.existsSync(path1)) {
        // read binary data
        var bitmap = fs.readFileSync(path1);
        // convert binary data to base64 encoded string
        return Buffer.from(bitmap).toString('base64');
    }    
} */

module.exports = router;

