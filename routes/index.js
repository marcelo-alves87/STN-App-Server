var express = require('express');
var multer = require('multer');
var fs = require('fs');
var router = express.Router();
var path = require("path");
var exec = require("child_process").exec;
const UPLOAD_PATH = '../python/';
var uuid = require('uuid')

var store = multer.diskStorage({
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
});


function unlinkSyncFile(fileName) {
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
}

function processEncodedFile(fileEncoded, res, typeProcess) {
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
}

// function to encode file data to base64 encoded string
function base64_encode(fileName) {
    path1 = path.resolve(__dirname, UPLOAD_PATH, fileName);
    if(fs.existsSync(path1)) {
        // read binary data
        var bitmap = fs.readFileSync(path1);
        // convert binary data to base64 encoded string
        return Buffer.from(bitmap).toString('base64');
    }    
}

router.post('/fileProcess', function(req,res) {
//   processEncodedFile(JSON.stringify(req.body.fileName), res, req.body.typeProcess);

    // 1 - Checar conexao com o instrumento

    // 2 - Calibrar o instrumento de forma eletronica, dado o arquivo de calibracao

    // 3 - Pegar o arquivo do instrumento e salva lo com Pi.csv

    // 4 - Usar Convert to Model para gerar a entrada da rede neural

    setTimeout(execPython_Conversion, 1000, res);
    

    // 5 - Executar a rede como parametro o model da etapa anterior
    

    // 6 - gerar o relatorio


   //res.json({'print' : 1 });
});

function execPython_Conversion(res) {
  
    exec('python3 ./python/ConvertToModel.py', (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
          
          setTimeout(execPython_RNN, 1000, res); 
        }
    });

    
}

function execPython_RNN(res) {
  
    exec('python3 ./python/Workshop.py', (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
            console.log(4);
            setTimeout(getMeanModeFromRNN, 1000, stdout, res);
          
        }
    });
}

            
function getMeanModeFromRNN(stdout, res) {
    param1 = JSON.parse(stdout);

    exec('python3 ./python/GetMeanMode.py ' + param1, (error, stdout, stderr) => {
        if (error) {
          console.log('Erro:')
          console.error(error);
        } else {
          stdout.replace('[','');
          stdout.replace(']','');
          stdout.replace('(','');
          stdout.replace(')','');  
          res.json(stdout);
        }
    });
}

router.post('/checkConnectionAndCalibrationStatus', function(req,res){
    /*
    0 - Sem conexao, 1 - Sem calibracao, 2 - Calibracao encontrada, e retornar a data da calibracao
    */
    
   checkConnection(res);

   
    /* if(data1 == 0) {
        res.json({'status' : 0});
    } else {
        data1 = setTimeout(checkCalibrationStatus, timeout1);
        console.log(data1);
    } */

  

    
    
});

function checkCalibrationStatus(res) {

    exec('python ./python/CheckCalibration.py', (error, stdout, stderr) => {
        if (error) {
          console.error(error);
        } 
        else if(stderr) {
          console.log(stderr)  
        }
        else {         
          if(stdout.trim() === 'erro') {
            res.json({'status' : 1});
          } else {  
            res.json({'status' : 2, 'date': stdout.trim()})
          }
        }
    });

}

function checkConnection(res) {


    exec('python ./python/CheckConnection.py', (error, stdout, stderr) => {
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
            checkCalibrationStatus(res);
           }
        }
    });
}

   


module.exports = router;