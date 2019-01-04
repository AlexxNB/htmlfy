# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import htmlfy

def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')


 
class TestHtmlfy(unittest.TestCase):

    def test_simplehtml(self):
        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Hello</title>
            </head>
            <body>
                <p>hello, world!</p>
            </body>
        </html>
        """
        html_minified = "<!DOCTYPE html><html><head><title>Hello</title></head><body><p>hello, world!</p></body></html>"
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_comments(self):
        html = """
        <!--This comment should be removed -->
        <!--! This comment will not be removed -->
        <!-- 
        ----  This comment should be removed 
        -->
        <!--[if gte IE 7]>Will not be removed<![endif]-->
        <a href="//google.com">Google</a>
        <script type="text/javascript">
            /* 
            *  This comment should be removed
            */
            a=1 //this comment should be removed 
            // comment should be removed
        </script>
        """
        html_minified ="""<!--! This comment will not be removed --><!--[if gte IE 7]>Will not be removed<![endif]--><a href="//google.com">Google</a><script type="text/javascript">
            a=1
        </script>"""
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_strict_spaces(self):
        html = """
        <p>Text      sample of   
            tooo many  
               spaces
        </p>
        """
        html_minified ="<p>Text sample of tooo many spaces</p>"
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_spaces_between_tags(self):
        html = """
        <p>
              <span>Text in tag1 </span> Text outside tags
            <span>Text in tag2     </span>
               <span>Text    in    tag3</span>
        </p>
        """
        html_minified ="<p><span>Text in tag1</span>Text outside tags<span>Text in tag2</span><span>Text in tag3</span></p>"
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_php_preserve(self):
        html = """
        <p>
            <ul>
            <?php for($i=1; $i <= 10; $i++):?>
                <li>This is line #<?=$i?></li>
            <?php endfor;?>
            </ul>
        </p>
        """
        html_minified ="<p><ul><?php for($i=1; $i <= 10; $i++):?><li>This is line #<?=$i?></li><?php endfor;?></ul></p>"
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_preserve_inside_tag(self):
        html = """
        <p class="myclass <?php if($Hidden):?>hide<?php endif;?>">
            Hidden
        </p>
        """
        html_minified ='<p class="myclass <?php if($Hidden):?>hide<?php endif;?>">Hidden</p>'
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_javascript_preserve(self):
        html = """<script type="text/javascript">
            for (i=1; i<=10; i++) {
                document.writeln("<p>This is line #"+i+"</p>")
            }
        </script>"""
        self.assertEqual(htmlfy.minify_html(html), html)

    def test_pre_preserve(self):
        html = """<pre>
                This text shoud be preserve.
                Save spaces    and    multilines.
            </pre>"""
        self.assertEqual(htmlfy.minify_html(html), html)

    
    def test_css_minify(self):
        html = """
        <style type="text/css">
        /* This comment should be removed */
        a{
            color: blue;
        }
        a:hover{
            color: gray;
        }

        </style>
        """
        html_minified ='<style type="text/css">a{color: blue;} a:hover{color: gray;}</style>'
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_html5_attributes_minification(self):
        html = """
        <input type="text" disabled="disabled">
        <input type="radio" checked="checked">
        <select>
            <option selected="selected">Option</option>
        </select>
        """
        html_minified ='<input type="text" disabled><input type="radio" checked><select><option selected>Option</option></select>'
        self.assertEqual(htmlfy.minify_html(html), html_minified)

    def test_html5_strip_slash_in_emptytags(self):
        html = """
        <input type="text"/>
        <br />
        """
        html_minified ='<input type="text"><br>'
        self.assertEqual(htmlfy.minify_html(html), html_minified)