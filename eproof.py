import argparse
import requests
import re

class Convert:
    def __init__(self,filename):
        self.filename=filename
        filename_list=filename.split('.')
        assert len(filename_list)>1, 'The file ({}) does not have an extension.'.format(filename)
        self.file='.'.join(filename_list[:-1])
        self.ext=filename_list[-1]
        self.alpha=0.5
        assert self.ext.lower()=='pdf', 'The file should be PDF.'
        self.api_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMmY1NjFjZThjYzgxZWMxMmYxYTJhZGUyMjEyZGI5ZTJkYWViNzViZGM1ZjNkNmVmYWMxZjUxYTAwNjY4MjkxZjQ5MmQ4ZmMwOGQ1Yzg3MjEiLCJpYXQiOjE2NDgwMDAwMDQuMDEzMjQ4LCJuYmYiOjE2NDgwMDAwMDQuMDEzMjUsImV4cCI6NDgwMzY3MzYwNC4wMDk1Niwic3ViIjoiNTY5MTU4OTQiLCJzY29wZXMiOlsidXNlci5yZWFkIiwidXNlci53cml0ZSIsInRhc2sucmVhZCIsInRhc2sud3JpdGUiLCJ3ZWJob29rLnJlYWQiLCJ3ZWJob29rLndyaXRlIiwicHJlc2V0LnJlYWQiLCJwcmVzZXQud3JpdGUiXX0.W4N0BBqxoQ6ex3TABRgs_DPcPHHxmtDk7SNGdfNzMPbajPL-HbPBrVailGajSLmpGiQO14TcQdNZ12id3fVet5CLrB4ncXwKpRgdU6GnFMNCgEgevGJpW3Vsjosnvau75reQbNgCxZU4FkePy4dg6UbHCDDNAhnRq-NtwC5tUnI4hQzMAlLoVeke3A_ahDEmrea1d0Xgzb_nVBi0eCFnEH61ggtiTkz2eGFNdifVnUCajfGpYZFc1rpC_qvwdKx5WPZmTh2Q9naB-xWn3JPJEKJyIN0yPSTmHjoJbwtlTkI_ZIsd_iWB-NXpCxomXsR_t7BpvfaW9ShTPYa0xV35W26Lr9YAUWXP5wnGTvyg4BPRT89C87xdRjXKmbKkuicZWA4GgZ2o9BLCWLM6IO3aRETUFobk0rhf2iu0HZRwQz3hHgMTNz2wMsP3HqTSEwg75Q4qv_r_qjoj4SmbQJ4UIT_7uZOFJaz4OnuOxmgAyGJ40Q4ZwyeEgs24aZiY8e0B42IRVTFofNzarZV0krHJ0xSa2xxK9_i60xdnnvH8VcGlCGvucBkbq8xUbZq7b5p3YZt0ELrbeKkHo8k_j3VAsMDqFzc0j92Hfr_KyLS4VeR5l_b5Oh7dx4FaN748fCtw1sKakjYOmSsXtByuHv07hZycdu_1Nv5hjLU6oym6o08'
        self.headers={'Authorization':'Bearer {}'.format(self.api_key),'Content-type': 'application/json'}

    def submit_job(self):
        body={
            "tasks": {
                "import-1": {
                    "operation": "import/upload",
                },
                "task-1": {
                    "operation": "convert",
                    "input_format": "pdf",
                    "output_format": "html",
                    "engine": "pdf2htmlex",
                    "input": [
                        "import-1"
                    ],
                    "outline": False,
                    "zoom": 1.5,
                    "embed_css": True,
                    "embed_javascript": True,
                    "embed_images": True,
                    "embed_fonts": True,
                    "split_pages": False,
                    "bg_format": "png"
                },
                "export-1": {
                    "operation": "export/url",
                    "input": [
                        "task-1"
                    ],
                    "inline": False,
                    "archive_multiple_files": False
                }
            },
            "tag": "jobbuilder"
        }        
        self.response_submit = requests.post('https://api.cloudconvert.com/v2/jobs',json=body,headers={'Authorization':'Bearer {}'.format(self.api_key)})

    def upload(self):
        response_submit_dict=self.response_submit.json()
        try:
            self.job_id=response_submit_dict['data']['id']
            form=response_submit_dict['data']['tasks'][0]['result']['form']
        except:
            raise ValueError(response_submit_dict['message'])
        port_url=form['url']
        params=form['parameters']
        file=open(self.filename,'rb')
        files={'file':file}
        requests.post(port_url,files=files,data=params)
        file.close()
        print('Converting to html...')

    def export(self):
        finished=requests.get('https://api.cloudconvert.com/v2/jobs/{}/wait'.format(self.job_id),headers=self.headers)
        download_url=finished.json()['data']['tasks'][0]['result']['files'][0]['url']
        download_filename=finished.json()['data']['tasks'][0]['result']['files'][0]['filename']
        self.downloads=requests.get(download_url)
        print('Finish converting to html.')

    def read_html(self):
        html_doc=self.downloads.content.decode('utf-8')
        colors=re.findall(r'\.fc[\d]\{.*\}',html_doc)
        for color in colors:
            cc=re.findall('color:rgb\((.*?)\);',color)[0]
            if '0,0,0' in cc:
                new_color=add_background(color,'white')
            else:
                new_color=add_background(color,r'rgb({},{})'.format(cc,self.alpha))
            html_doc=html_doc.replace(color, new_color)
        with open('{}.html'.format(self.file),'w',encoding='utf-8') as f:
            f.write(html_doc)

def add_background(color,background):
    if 'background-color' not in color:
        return color.replace(r'}','background-color: {} ;}}'.format(background))
    else:
        return color

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-fn',type=str,help='File name')
    args=parser.parse_args()
    convert=Convert(args.fn)
    convert.submit_job()
    convert.upload()
    convert.export()
    convert.read_html()
